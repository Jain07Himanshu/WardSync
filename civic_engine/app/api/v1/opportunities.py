"""Civic Opportunities, action generation, and human review endpoints."""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import CivicOpportunity, ConsolidatedIssue
from app.schemas.opportunity import (
    CivicOpportunityResponse,
    CivicOpportunityListResponse,
    OpportunityReviewRequest,
    OpportunityReviewResponse,
)
from app.opportunities.service import OpportunityService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Opportunities"])


def _to_opportunity_response(opp: CivicOpportunity, issue_title: Optional[str] = None) -> CivicOpportunityResponse:
    title = issue_title or (opp.issue.title if opp.issue else None)
    return CivicOpportunityResponse(
        id=opp.id,
        issue_id=opp.issue_id,
        issue_title=title,
        title=opp.title,
        problem_summary=opp.problem_summary,
        why_needed=opp.why_needed,
        activity_type=opp.activity_type,
        step_by_step_plan=opp.step_by_step_plan or [],
        intended_beneficiaries=opp.intended_beneficiaries,
        suggested_roles=opp.suggested_roles or [],
        required_materials=opp.required_materials or [],
        estimated_effort_hours=opp.estimated_effort_hours,
        suggested_participant_count=opp.suggested_participant_count,
        potential_collaborators=opp.potential_collaborators or [],
        escalation_channel=opp.escalation_channel,
        expected_outcomes=opp.expected_outcomes,
        success_metrics=opp.success_metrics,
        safety_considerations=opp.safety_considerations or [],
        prerequisites_and_permissions=opp.prerequisites_and_permissions or [],
        is_official_authorization_required=opp.is_official_authorization_required,
        safety_risk_level=opp.safety_risk_level,
        ai_confidence=opp.ai_confidence,
        review_status=opp.review_status,
        review_notes=opp.review_notes,
        priority_score=opp.priority_score,
        priority_breakdown=opp.priority_breakdown or {},
        created_at=opp.created_at,
        updated_at=opp.updated_at,
    )


@router.post("/issues/{issue_id}/opportunities/generate", response_model=List[CivicOpportunityResponse], summary="Generate civic opportunities for an issue")
def generate_opportunities_endpoint(issue_id: str, db: Session = Depends(get_db)):
    """
    Generate constructive, safe citizen action opportunities and volunteer tasks
    grounded in the evidentiary findings of the consolidated civic issue.
    """
    service = OpportunityService(db)
    try:
        created = service.generate_opportunities_for_issue(issue_id)
        return [_to_opportunity_response(o) for o in created]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/opportunities", response_model=CivicOpportunityListResponse, summary="List civic action opportunities")
def list_opportunities(
    review_status: Optional[str] = Query(None, description="PENDING_REVIEW, APPROVED, REJECTED"),
    activity_type: Optional[str] = Query(None, description="EVIDENCE_COLLECTION, COMMUNITY_SURVEY, etc."),
    issue_id: Optional[str] = Query(None, description="Filter by linked civic issue ID"),
    safety_risk_level: Optional[str] = Query(None, description="LOW, MODERATE, HIGH_REQUIRES_AUTHORITY"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve paginated civic opportunities sorted by priority score."""
    query = db.query(CivicOpportunity)

    if review_status:
        query = query.filter(CivicOpportunity.review_status == review_status)
    if activity_type:
        query = query.filter(CivicOpportunity.activity_type == activity_type)
    if issue_id:
        query = query.filter(CivicOpportunity.issue_id == issue_id)
    if safety_risk_level:
        query = query.filter(CivicOpportunity.safety_risk_level == safety_risk_level)

    total = query.count()
    items = query.order_by(CivicOpportunity.priority_score.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return CivicOpportunityListResponse(
        items=[_to_opportunity_response(o) for o in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/opportunities/{opportunity_id}", response_model=CivicOpportunityResponse, summary="Get opportunity details")
def get_opportunity(opportunity_id: str, db: Session = Depends(get_db)):
    """Fetch complete details, safety requirements, and action plan for a volunteer opportunity."""
    opp = db.query(CivicOpportunity).filter(CivicOpportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail=f"CivicOpportunity {opportunity_id} not found.")
    return _to_opportunity_response(opp)


@router.post("/opportunities/{opportunity_id}/review", response_model=OpportunityReviewResponse, summary="Review and moderate opportunity")
def review_opportunity_endpoint(
    opportunity_id: str,
    payload: OpportunityReviewRequest,
    db: Session = Depends(get_db),
):
    """
    Submit a human moderation decision (APPROVED, REJECTED, MODIFIED) on a generated opportunity.
    Ensures that high-impact or safety-critical actions are reviewed before public deployment.
    """
    service = OpportunityService(db)
    try:
        review_audit = service.review_opportunity(opportunity_id, payload)
        return OpportunityReviewResponse.model_validate(review_audit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
