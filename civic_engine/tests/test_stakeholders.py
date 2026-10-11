"""Tests for stakeholder discovery and verification status integrity."""

from app.models.models import ConsolidatedIssue
from app.stakeholders.service import StakeholderService


def test_stakeholder_discovery_verified_match(db_session):
    issue = ConsolidatedIssue(
        title="Severe Potholes on S.V. Road",
        summary="Deep potholes disrupting vehicular flow.",
        category="Roads and potholes",
        normalized_location="Andheri West, Mumbai",
        jurisdiction_name="Brihanmumbai Municipal Corporation (BMC)",
        ward_zone="K-West",
    )
    db_session.add(issue)
    db_session.commit()

    service = StakeholderService(db_session)
    result = service.discover_stakeholders_for_issue(issue.id)

    assert result.issue_id == issue.id
    assert len(result.stakeholders) >= 1

    # Check verified BMC department
    bmc_stakeholder = next((s for s in result.stakeholders if "Brihanmumbai" in s.candidate_name or "BMC" in s.candidate_name), None)
    assert bmc_stakeholder is not None
    assert bmc_stakeholder.verification_status == "VERIFIED_REGISTRY"
    assert bmc_stakeholder.public_helpline == "1916"
    assert "https://" in bmc_stakeholder.official_website


def test_stakeholder_candidate_unverified_no_fake_phone(db_session):
    issue = ConsolidatedIssue(
        title="Unusual community concern",
        summary="Novel public amenity defect.",
        category="Other emerging civic concerns",
        normalized_location="Unknown Corridor",
    )
    db_session.add(issue)
    db_session.commit()

    service = StakeholderService(db_session)
    result = service.discover_stakeholders_for_issue(issue.id)

    for stk in result.stakeholders:
        if stk.verification_status == "CANDIDATE_UNVERIFIED":
            # Strict anti-hallucination check: Phone number must NOT be invented
            assert stk.public_helpline is None
            assert stk.public_email is None
