"""Health, configuration status, and background job inspection endpoints."""

import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.models import SourceProcessingJob
from app.schemas.source import SourceProcessingJobResponse

router = APIRouter(tags=["Health & Status"])


@router.get("/health", summary="Service health check")
def health_check() -> Dict[str, Any]:
    """Verify backend engine is operational and return system timestamp."""
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }


@router.get("/config/status", summary="Safe system configuration inspection")
def get_config_status() -> Dict[str, Any]:
    """
    Expose safe, non-sensitive system configuration, active AI provider,
    and configured credentials status. Never returns secret keys.
    """
    return settings.get_safe_status()


@router.get("/jobs/{job_id}", response_model=SourceProcessingJobResponse, summary="Inspect background processing job")
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """Retrieve execution status and progress of an asynchronous pipeline job."""
    job = db.query(SourceProcessingJob).filter(SourceProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return job
