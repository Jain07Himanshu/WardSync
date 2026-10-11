"""Stakeholder discovery and mapping API endpoints."""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import ConsolidatedIssue, IssueStakeholderMapping
from app.schemas.stakeholder import (
    IssueStakeholderResponse,
    StakeholderDiscoveryResult,
)
from app.stakeholders.service import StakeholderService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Stakeholders"])


@router.get("/issues/{issue_id}/stakeholders", response_model=List[IssueStakeholderResponse], summary="List stakeholders for an issue")
def get_issue_stakeholders(issue_id: str, db: Session = Depends(get_db)):
    """Retrieve authorities and civic organizations currently mapped to an issue."""
    issue = db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail=f"ConsolidatedIssue {issue_id} not found.")

    mappings = db.query(IssueStakeholderMapping).filter(IssueStakeholderMapping.issue_id == issue.id).all()
    results = []
    for m in mappings:
        stk = m.stakeholder
        results.append(
            IssueStakeholderResponse(
                id=m.id,
                issue_id=m.issue_id,
                stakeholder_id=m.stakeholder_id,
                candidate_name=m.candidate_name,
                department=stk.department if stk else None,
                relevance_reason=m.relevance_reason,
                jurisdiction_coverage=m.jurisdiction_coverage,
                official_website=stk.official_website if stk else None,
                public_portal_url=stk.public_portal_url if stk else None,
                public_helpline=stk.public_helpline if stk else None,
                public_email=stk.public_email if stk else None,
                grievance_redressal_mechanism=stk.grievance_redressal_mechanism if stk else None,
                verification_status=m.verification_status,
                confidence_level=m.confidence_level,
                source_reference=m.source_reference,
                created_at=m.created_at,
            )
        )
    return results


@router.post("/issues/{issue_id}/stakeholders/discover", response_model=StakeholderDiscoveryResult, summary="Discover authorities and stakeholders")
def discover_stakeholders_endpoint(issue_id: str, db: Session = Depends(get_db)):
    """
    Query verified municipal directory and AI governance module to identify
    responsible authorities, ward offices, and relevant public NGOs.
    """
    service = StakeholderService(db)
    try:
        return service.discover_stakeholders_for_issue(issue_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
