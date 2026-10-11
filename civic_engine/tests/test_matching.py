"""Tests for issue matching, deduplication, and recurring issue detection."""

from datetime import datetime, timedelta
from app.location.resolver import haversine_distance_km, resolve_location
from app.matching.engine import compute_text_similarity, evaluate_issue_pair
from app.schemas.common import IssueRelationshipType
from app.models.models import ExtractedIssueObservation, Source
from app.matching.service import MatchingService


def test_haversine_distance():
    # Andheri West (19.1197, 72.8468) to Andheri East (19.1136, 72.8697) is roughly 2.5 km
    dist = haversine_distance_km(19.1197, 72.8468, 19.1136, 72.8697)
    assert 2.0 < dist < 3.0

    # Same coordinate distance should be 0.0
    assert haversine_distance_km(19.1197, 72.8468, 19.1197, 72.8468) == 0.0


def test_resolve_location():
    loc = resolve_location("Huge crater outside Andheri West railway station")
    assert loc["normalized_location"] == "Andheri West, Mumbai"
    assert loc["ward_zone"] == "K-West"
    assert loc["is_geocoded"] is True


def test_evaluate_duplicate_report():
    date1 = datetime(2026, 9, 15)
    date2 = datetime(2026, 9, 16)
    res = evaluate_issue_pair(
        title1="Deep crater on S.V. Road Andheri",
        desc1="Dangerous pothole observed near station junction.",
        cat1="Roads and potholes",
        loc1="Andheri West, Mumbai",
        lat1=19.1197,
        lon1=72.8468,
        date1=date1,
        title2="Pothole near Andheri station",
        desc2="Two-wheeler accident risk due to deep crater.",
        cat2="Roads and potholes",
        loc2="Andheri West, Mumbai",
        lat2=19.1197,
        lon2=72.8468,
        date2=date2,
    )
    assert res.relationship_type == IssueRelationshipType.DUPLICATE_REPORT
    assert res.is_merge_candidate is True
    assert res.similarity_score >= 0.8


def test_evaluate_recurring_incident():
    # Same location and category, but 45 days apart
    date1 = datetime(2026, 8, 1)
    date2 = datetime(2026, 9, 15)
    res = evaluate_issue_pair(
        title1="Subway flooding at Milan Subway",
        desc1="Severe waterlogging after monsoon rainfall.",
        cat1="Drainage and waterlogging",
        loc1="Milan Subway, Santacruz West, Mumbai",
        lat1=19.0833,
        lon1=72.8367,
        date1=date1,
        title2="Milan Subway inundated again",
        desc2="Underpass shut for traffic following morning rain.",
        cat2="Drainage and waterlogging",
        loc2="Milan Subway, Santacruz West, Mumbai",
        lat2=19.0833,
        lon2=72.8367,
        date2=date2,
    )
    assert res.relationship_type == IssueRelationshipType.RECURRING_INCIDENT
    assert res.is_merge_candidate is True


def test_evaluate_unrelated_keyword_match():
    res = evaluate_issue_pair(
        title1="Potholes on road",
        desc1="Dangerous craters on asphalt roadway.",
        cat1="Roads and potholes",
        loc1="Andheri West",
        lat1=19.1197,
        lon1=72.8468,
        date1=datetime.utcnow(),
        title2="Grand heritage road show and cultural festival",
        desc2="Vintage vehicles parade on the road.",
        cat2="Other emerging civic concerns",
        loc2="Marine Drive",
        lat2=18.9400,
        lon2=72.8200,
        date2=datetime.utcnow(),
    )
    assert res.relationship_type == IssueRelationshipType.UNRELATED_KEYWORD_MATCH
    assert res.is_merge_candidate is False


def test_consolidation_service(db_session):
    src1 = Source(
        source_type="user_text",
        original_title="Report 1",
        extracted_text="Potholes on S.V. Road Andheri",
        content_hash="hash1",
        language="en",
    )
    db_session.add(src1)
    db_session.flush()

    obs1 = ExtractedIssueObservation(
        source_id=src1.id,
        issue_title="Severe Potholes on S.V. Road",
        problem_description="Crater on road slowing traffic.",
        category="Roads and potholes",
        normalized_location="Andheri West, Mumbai",
        latitude=19.1197,
        longitude=72.8468,
        most_recent_observation_date=datetime(2026, 9, 15),
    )
    db_session.add(obs1)
    db_session.commit()

    matcher = MatchingService(db_session)
    consolidated = matcher.consolidate_unassigned_observations()
    assert len(consolidated) == 1
    assert consolidated[0].observation_count == 1

    # Now add second observation describing same incident
    src2 = Source(
        source_type="user_text",
        original_title="Report 2",
        extracted_text="Dangerous crater near Andheri West",
        content_hash="hash2",
        language="en",
    )
    db_session.add(src2)
    db_session.flush()

    obs2 = ExtractedIssueObservation(
        source_id=src2.id,
        issue_title="Dangerous Crater near Andheri Station",
        problem_description="Vehicular slowdown due to pothole on S.V. Road.",
        category="Roads and potholes",
        normalized_location="Andheri West, Mumbai",
        latitude=19.1197,
        longitude=72.8468,
        most_recent_observation_date=datetime(2026, 9, 16),
    )
    db_session.add(obs2)
    db_session.commit()

    consolidated2 = matcher.consolidate_unassigned_observations()
    assert len(consolidated2) == 1
    # Observation count should now be 2 for the same consolidated issue!
    assert consolidated2[0].observation_count == 2
