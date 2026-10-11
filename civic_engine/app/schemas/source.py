"""Schemas for Source ingestion and processing."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from app.schemas.common import SourceType, ProcessingStatus


class SourceCreate(BaseModel):
    """Payload to submit a text or URL for ingestion."""
    source_type: SourceType = Field(default=SourceType.USER_TEXT, description="Type of source input")
    original_title: str = Field(..., min_length=3, max_length=500, description="Title or headline")
    extracted_text: Optional[str] = Field(default=None, description="Raw text if submitted directly")
    original_url: Optional[str] = Field(default=None, description="Public URL or RSS endpoint")
    publisher: Optional[str] = Field(default="Public User Submission", description="Publishing organization or newspaper")
    publication_date: Optional[datetime] = Field(default=None, description="Date source was originally published")
    metadata_payload: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary source metadata")


class SourceResponse(BaseModel):
    """Normalized common source format output."""
    id: str
    source_type: str
    original_title: str
    original_url_or_ref: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[datetime] = None
    retrieval_timestamp: datetime
    extracted_text_preview: str
    language: str
    content_hash: str
    processing_status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SourceDetailResponse(SourceResponse):
    """Detailed view including full extracted text and observation count."""
    extracted_text: str
    observations_count: int = 0
    metadata_payload: Dict[str, Any] = Field(default_factory=dict)


class SourceProcessingJobResponse(BaseModel):
    """Status of asynchronous source ingestion or extraction job."""
    id: str
    job_type: str
    status: str
    source_id: Optional[str] = None
    issue_id: Optional[str] = None
    progress_percentage: int
    total_items: int
    processed_items: int
    error_details: Optional[str] = None
    result_summary: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SourceListResponse(BaseModel):
    """Paginated collection of sources."""
    items: List[SourceResponse]
    total: int
    page: int
    page_size: int
