"""Tests for civic action generation, safety guardrails, and prioritization."""

from app.models.models import ConsolidatedIssue, CivicOpportunity
from app.opportunities.service import OpportunityService
from app.prioritization.service import PrioritizationService
from app.schemas.opportunity import OpportunityReviewRequest, OpportunityReviewStatus


def test_opportunity_prioritization_weights():
    prioritizer = PrioritizationService()
    score, breakdown = prioritizer.compute_opportunity_priority(
        severity_score=8.0,
        community_impact_score=7.0,
        urgency_score=8.0,
        recurrence_score=6.0,
        evidence_strength_score=9.0,
        feasibility_score=8.0,
        safety_risk_level="LOW",
    )
    assert 50.0 <= score <= 100.0
    assert "weights" in breakdown
    assert "components" in breakdown
    assert breakdown["requires_human_review"] is False


def test_opportunity_generation_and_safety_guardrail(db_session):
    issue = ConsolidatedIssue(
        title="Severe Potholes on S.V. Road",
        summary="Craters causing skidding hazards on arterial street.",
        category="Roads and potholes",
        normalized_location="Andheri West, Mumbai",
        severity_score=7.5,
        urgency_score=7.0,
        recurrence_score=5.0,
        evidence_strength_score=8.0,
        community_impact_score=7.0,
    )
    db_session.add(issue)
    db_session.commit()

    service = OpportunityService(db_session)
    opps = service.generate_opportunities_for_issue(issue.id)

    assert len(opps) >= 1
    opp = opps[0]
    assert opp.issue_id == issue.id
    assert opp.priority_score > 40.0
    assert len(opp.safety_considerations) >= 1
    assert "Never step into active vehicular traffic" in " ".join(opp.safety_considerations)


def test_opportunity_review_workflow(db_session):
    issue = ConsolidatedIssue(
        title="Overflowing Solid Waste",
        summary="Roadside garbage pile on Link Road.",
        category="Waste management",
        normalized_location="Malad West, Mumbai",
    )
    db_session.add(issue)
    db_session.commit()

    service = OpportunityService(db_session)
    opps = service.generate_opportunities_for_issue(issue.id)
    opp_id = opps[0].id

    # Review to APPROVED
    review_req = OpportunityReviewRequest(
        reviewer_name="Civic Admin Moderator",
        status=OpportunityReviewStatus.APPROVED,
        feedback_comments="Verified safe citizen photo survey protocol.",
    )
    review_record = service.review_opportunity(opp_id, review_req)
    assert review_record.status == "APPROVED"

    updated_opp = db_session.query(CivicOpportunity).filter(CivicOpportunity.id == opp_id).first()
    assert updated_opp.review_status == "APPROVED"
