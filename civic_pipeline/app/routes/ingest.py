import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from ..models.schemas import (
    MultiSourceIngestRequest,
    IngestPipelineResult,
    CivicSourceOut,
    CivicIssueOut,
    NGOVolunteerEventOut,
    AlertPayload,
)
from ..ai.clustering_engine import get_clustering_engine
from ..ai.ngo_dispatcher import get_ngo_dispatcher

logger = logging.getLogger("civic_pipeline.routes.ingest")
router = APIRouter(prefix="/api/ingest", tags=["Ingestion & Verification"])


@router.post(
    "/multi-source",
    response_model=IngestPipelineResult,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest multi-source signals, run AI verification, cluster issues, and dispatch NGO events"
)
async def ingest_multi_source_signals(payload: MultiSourceIngestRequest) -> IngestPipelineResult:
    """
    Accepts an array of raw text signals (social media posts, e-news articles, resident complaints,
    municipal notices) and executes the automated 4-step pipeline:
    1. Ingestion and persistence of raw signals into `civic_sources`.
    2. Google Gemini 1.5 Flash structured synthesis, metadata extraction, and authenticity scoring.
    3. text-embedding-004 vector embedding computation & pgvector cosine similarity clustering.
    4. Automated NGO matching and draft volunteer event creation if verified (authenticity >= 65).
    """
    if not payload.signals:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signals list cannot be empty."
        )

    try:
        clustering_engine = get_clustering_engine()
        dispatcher = get_ngo_dispatcher()

        # Step 1, 2, 3: Ingest, Verify, and Cluster
        issue_record, cluster_action, sim_score, saved_sources = clustering_engine.process_and_cluster(
            payload.signals
        )

        # Step 4: Dispatch to matching NGOs if verified (authenticity >= 65)
        dispatched_events = []
        ngo_alerts = []
        if issue_record.get("authenticity_score", 0) >= 65:
            events_data, alerts = dispatcher.dispatch_verified_issue(issue_record)
            dispatched_events = [NGOVolunteerEventOut(**e) for e in events_data]
            ngo_alerts = alerts

        # Format output
        sources_out = [
            CivicSourceOut(
                id=UUID(s["id"]),
                issue_id=UUID(s["issue_id"]) if s.get("issue_id") else None,
                source_type=s["source_type"],
                source_url=s.get("source_url"),
                raw_content=s["raw_content"],
                published_at=s["published_at"],
                status=s.get("status", "processed"),
                created_at=s["created_at"]
            )
            for s in saved_sources
        ]

        issue_out = CivicIssueOut(
            id=UUID(issue_record["id"]),
            title=issue_record["title"],
            summary=issue_record["summary"],
            category=issue_record["category"],
            ward=issue_record["ward"],
            latitude=issue_record["latitude"],
            longitude=issue_record["longitude"],
            severity=issue_record["severity"],
            authenticity_score=issue_record["authenticity_score"],
            verification_reasoning=issue_record.get("verification_reasoning"),
            responsible_authority=issue_record["responsible_authority"],
            source_count=issue_record.get("source_count", 1),
            status=issue_record.get("status", "flagged_unverified"),
            created_at=issue_record["created_at"],
            updated_at=issue_record.get("updated_at")
        )

        return IngestPipelineResult(
            ingested_source_count=len(saved_sources),
            sources=sources_out,
            issue=issue_out,
            cluster_action=cluster_action,
            similarity_score=sim_score,
            authenticity_score=issue_record["authenticity_score"],
            dispatched_events=dispatched_events,
            ngo_alerts=ngo_alerts
        )

    except Exception as e:
        logger.exception("Ingestion pipeline failure: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline processing error: {str(e)}"
        )
