"""Source ingestion endpoints for text, URLs, and uploaded documents."""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import UnsupportedFileTypeError, IngestionError
from app.models.models import Source, SourceProcessingJob
from app.schemas.source import (
    SourceCreate,
    SourceResponse,
    SourceDetailResponse,
    SourceListResponse,
    SourceProcessingJobResponse,
)
from app.ingestion.service import IngestionService
from app.workers.pipeline import run_full_pipeline_for_source

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sources", tags=["Sources"])


def _to_source_response(source: Source) -> SourceResponse:
    return SourceResponse(
        id=source.id,
        source_type=source.source_type,
        original_title=source.original_title,
        original_url_or_ref=source.original_url_or_ref,
        publisher=source.publisher,
        publication_date=source.publication_date,
        retrieval_timestamp=source.retrieval_timestamp,
        extracted_text_preview=source.extracted_text[:250] + ("..." if len(source.extracted_text) > 250 else ""),
        language=source.language,
        content_hash=source.content_hash,
        processing_status=source.processing_status,
        error_message=source.error_message,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )


@router.post("", response_model=SourceResponse, summary="Ingest raw text or public URL")
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    """
    Ingest a public news article, RSS item, or user complaint text into the engine.
    Normalizes content into standard source format with SHA-256 deduplication.
    """
    ingestion = IngestionService(db)
    try:
        if payload.original_url:
            if payload.source_type.value == "rss":
                sources = ingestion.ingest_rss(str(payload.original_url))
                source = sources[0] if sources else None
                if not source:
                    raise HTTPException(status_code=400, detail="No entries parsed from RSS feed.")
            else:
                source = ingestion.ingest_url(str(payload.original_url), publisher=payload.publisher)
        elif payload.extracted_text:
            source = ingestion.ingest_text(
                title=payload.original_title,
                text=payload.extracted_text,
                publisher=payload.publisher or "User Submission",
                metadata=payload.metadata_payload,
            )
        else:
            raise HTTPException(status_code=400, detail="Either extracted_text or original_url must be provided.")

        return _to_source_response(source)
    except IngestionError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/upload", response_model=SourceResponse, summary="Upload document (PDF, DOCX, CSV, TXT)")
async def upload_document(
    file: UploadFile = File(...),
    publisher: Optional[str] = Form("Uploaded Document"),
    db: Session = Depends(get_db),
):
    """
    Upload and parse an evidentiary document (PDF, DOCX, CSV, TXT, MD).
    Restricted to configured file extensions and size limit (10MB).
    """
    file_bytes = await file.read()
    if len(file_bytes) > settings.FILE_UPLOAD_MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"File exceeds maximum allowed size of {settings.FILE_UPLOAD_MAX_BYTES // (1024*1024)}MB.")

    ingestion = IngestionService(db)
    try:
        source = ingestion.ingest_file(
            filename=file.filename or "uploaded_file",
            file_bytes=file_bytes,
            publisher=publisher or "Uploaded Document",
        )
        return _to_source_response(source)
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=415, detail=str(e))
    except IngestionError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("", response_model=SourceListResponse, summary="List ingested sources")
def list_sources(
    source_type: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve paginated collection of normalized sources with optional filtering."""
    query = db.query(Source)
    if source_type:
        query = query.filter(Source.source_type == source_type)
    if status:
        query = query.filter(Source.processing_status == status)

    total = query.count()
    items = query.order_by(Source.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return SourceListResponse(
        items=[_to_source_response(s) for s in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{source_id}", response_model=SourceDetailResponse, summary="Get source details and full text")
def get_source(source_id: str, db: Session = Depends(get_db)):
    """Fetch complete source record including full extracted text and observation count."""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail=f"Source {source_id} not found.")

    obs_count = len(source.observations) if source.observations else 0
    return SourceDetailResponse(
        id=source.id,
        source_type=source.source_type,
        original_title=source.original_title,
        original_url_or_ref=source.original_url_or_ref,
        publisher=source.publisher,
        publication_date=source.publication_date,
        retrieval_timestamp=source.retrieval_timestamp,
        extracted_text_preview=source.extracted_text[:250] + "...",
        extracted_text=source.extracted_text,
        language=source.language,
        content_hash=source.content_hash,
        processing_status=source.processing_status,
        error_message=source.error_message,
        metadata_payload=source.metadata_payload or {},
        observations_count=obs_count,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )


@router.post("/{source_id}/process", response_model=SourceProcessingJobResponse, summary="Trigger AI processing on source")
def process_source_endpoint(
    source_id: str,
    background_tasks: BackgroundTasks,
    run_async: bool = Query(True, description="Run in background and return job ID"),
    db: Session = Depends(get_db),
):
    """
    Execute the AI pipeline (issue extraction, consolidation, stakeholder discovery, opportunities)
    for a normalized source. Returns a trackable Job ID.
    """
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail=f"Source {source_id} not found.")

    job = SourceProcessingJob(
        job_type="FULL_PIPELINE",
        status="PENDING",
        source_id=source.id,
        progress_percentage=0,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    if run_async:
        background_tasks.add_task(run_full_pipeline_for_source, source_id=source.id, job_id=job.id)
    else:
        # Run synchronously
        run_full_pipeline_for_source(source_id=source.id, job_id=job.id)
        db.refresh(job)

    return job
