"""Civic Issue endpoints for discovery, intelligence, consolidation, and evidence."""

import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import (
    ConsolidatedIssue,
    ExtractedIssueObservation,
    Source,
    SourceProcessingJob,
)
from app.schemas.issue import (
    ConsolidatedIssueResponse,
    ConsolidatedIssueDetailResponse,
    ConsolidatedIssueListResponse,
    ObservationResponse,
    RelatedIssueMatchSchema,
    IssueEvidenceResponse,
    IssueEvidenceItem,
)
from app.extraction.service import ExtractionService
from app.matching.service import MatchingService
from app.intelligence.service import IntelligenceService
from app.workers.pipeline import run_full_pipeline_for_source

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Civic Issues"])


@router.post("/discovery/run", summary="Trigger proactive discovery cycle")
def run_discovery_cycle(
    background_tasks: BackgroundTasks,
    run_async: bool = Query(True, description="Execute in background"),
    db: Session = Depends(get_db),
):
    """
    Scan pending unprocessed sources, execute extraction, deduplication,
    stakeholder mapping, and opportunity generation across the pipeline.
    """
    pending_sources = db.query(Source).filter(Source.processing_status.in_(["PENDING", "PARSED"])).all()
    job_ids = []

    for src in pending_sources:
        job = SourceProcessingJob(
            job_type="DISCOVERY_BATCH",
            status="PENDING",
            source_id=src.id,
            progress_percentage=0,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        job_ids.append(job.id)

        if run_async:
            background_tasks.add_task(run_full_pipeline_for_source, source_id=src.id, job_id=job.id)
        else:
            run_full_pipeline_for_source(source_id=src.id, job_id=job.id)

    return {
        "status": "discovery_initiated",
        "pending_sources_queued": len(pending_sources),
        "job_ids": job_ids,
        "message": f"Queued {len(pending_sources)} sources for AI discovery and intelligence generation.",
    }


@router.post("/issues/analyze", summary="Analyze unassigned observations into consolidated issues")
def analyze_and_consolidate(db: Session = Depends(get_db)):
    """
    Run deduplication and semantic clustering on unassigned observations,
    forming or updating consolidated issues and intelligence scores.
    """
    matcher = MatchingService(db)
    consolidated = matcher.consolidate_unassigned_observations()

    intel_service = IntelligenceService(db)
    for issue in consolidated:
        intel_service.analyze_consolidated_issue(issue.id)
        matcher.find_related_issues(issue.id)

    return {
        "status": "completed",
        "consolidated_issues_count": len(consolidated),
        "issue_ids": [i.id for i in consolidated],
    }


@router.get("/issues", response_model=ConsolidatedIssueListResponse, summary="List consolidated civic issues")
def list_consolidated_issues(
    category: Optional[str] = Query(None, description="Filter by civic category"),
    is_recurring: Optional[bool] = Query(None, description="Filter recurring issues"),
    min_priority: Optional[float] = Query(None, ge=0, le=100, description="Minimum composite priority score"),
    search: Optional[str] = Query(None, description="Search keyword in title or location"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve consolidated civic issues with rich multi-factor filtering."""
    query = db.query(ConsolidatedIssue)

    if category:
        query = query.filter(ConsolidatedIssue.category == category)
    if is_recurring is not None:
        query = query.filter(ConsolidatedIssue.is_recurring == is_recurring)
    if min_priority is not None:
        query = query.filter(ConsolidatedIssue.composite_priority_score >= min_priority)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (ConsolidatedIssue.title.ilike(search_filter)) |
            (ConsolidatedIssue.normalized_location.ilike(search_filter)) |
            (ConsolidatedIssue.summary.ilike(search_filter))
        )

    total = query.count()
    items = query.order_by(ConsolidatedIssue.composite_priority_score.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return ConsolidatedIssueListResponse(
        items=[ConsolidatedIssueResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/issues/{issue_id}", response_model=ConsolidatedIssueDetailResponse, summary="Get consolidated issue details")
def get_consolidated_issue(issue_id: str, db: Session = Depends(get_db)):
    """Fetch complete civic intelligence dossier for an issue including linked observations."""
    issue = db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail=f"ConsolidatedIssue {issue_id} not found.")

    observations = db.query(ExtractedIssueObservation).filter(
        ExtractedIssueObservation.consolidated_issue_id == issue.id
    ).all()

    obs_responses = [ObservationResponse.model_validate(o) for o in observations]

    resp = ConsolidatedIssueDetailResponse(
        id=issue.id,
        title=issue.title,
        summary=issue.summary,
        category=issue.category,
        subcategory=issue.subcategory,
        normalized_location=issue.normalized_location,
        latitude=issue.latitude,
        longitude=issue.longitude,
        jurisdiction_name=issue.jurisdiction_name,
        ward_zone=issue.ward_zone,
        observation_count=issue.observation_count,
        distinct_publishers_count=issue.distinct_publishers_count,
        first_seen_date=issue.first_seen_date,
        last_seen_date=issue.last_seen_date,
        is_recurring=issue.is_recurring,
        recurrence_pattern=issue.recurrence_pattern,
        trend_direction=issue.trend_direction,
        verification_level=issue.verification_level,
        composite_priority_score=issue.composite_priority_score,
        severity_score=issue.severity_score,
        urgency_score=issue.urgency_score,
        recurrence_score=issue.recurrence_score,
        evidence_strength_score=issue.evidence_strength_score,
        community_impact_score=issue.community_impact_score,
        actionability_score=issue.actionability_score,
        what_is_happening=issue.what_is_happening,
        where_is_it_happening=issue.where_is_it_happening,
        unverified_information=issue.unverified_information or [],
        affected_stakeholders_summary=issue.affected_stakeholders_summary,
        recommended_practical_action=issue.recommended_practical_action,
        score_reasons=issue.score_reasons or {},
        observations=obs_responses,
        opportunities_count=len(issue.opportunities) if issue.opportunities else 0,
        stakeholders_count=len(issue.stakeholders) if issue.stakeholders else 0,
        created_at=issue.created_at,
        updated_at=issue.updated_at,
    )
    return resp


@router.post("/issues/{issue_id}/find-related", response_model=List[RelatedIssueMatchSchema], summary="Discover related issues")
def find_related_issues_endpoint(issue_id: str, db: Session = Depends(get_db)):
    """
    Run multi-factor matching to identify related incidents (duplicate reports,
    recurring problems, nearby similar issues, and cross-area parallels).
    """
    matcher = MatchingService(db)
    try:
        matches = matcher.find_related_issues(issue_id)
        return [RelatedIssueMatchSchema(**m) for m in matches]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/issues/{issue_id}/evidence", response_model=IssueEvidenceResponse, summary="Get full evidentiary dossier")
def get_issue_evidence(issue_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all source citations, verbatim quotes, and corroboration metrics
    supporting this consolidated civic issue without losing provenance.
    """
    issue = db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail=f"ConsolidatedIssue {issue_id} not found.")

    observations = db.query(ExtractedIssueObservation).filter(
        ExtractedIssueObservation.consolidated_issue_id == issue.id
    ).all()

    evidence_items: List[IssueEvidenceItem] = []
    unverified_facts = set()
    distinct_sources = set()

    for obs in observations:
        source = db.query(Source).filter(Source.id == obs.source_id).first()
        if source:
            distinct_sources.add(source.id)
            evidence_items.append(
                IssueEvidenceItem(
                    observation_id=obs.id,
                    source_id=source.id,
                    source_title=source.original_title,
                    publisher=source.publisher,
                    publication_date=source.publication_date,
                    source_url_or_ref=source.original_url_or_ref,
                    evidence_excerpts=obs.evidence_excerpts or [],
                    possible_causes=obs.possible_causes or [],
                    reported_consequences=obs.reported_consequences or [],
                    missing_information=obs.missing_information or [],
                    confidence_score=obs.confidence_score,
                )
            )
        if obs.missing_information:
            unverified_facts.update(obs.missing_information)

    corroboration = (
        f"Corroborated across {len(distinct_sources)} independent source(s) with {len(evidence_items)} direct observations."
        if len(distinct_sources) > 1
        else "Preliminary single-source report awaiting additional corroboration."
    )

    return IssueEvidenceResponse(
        issue_id=issue.id,
        issue_title=issue.title,
        distinct_sources_count=len(distinct_sources),
        evidence_items=evidence_items,
        unverified_facts=list(unverified_facts),
        corroboration_summary=corroboration,
    )
