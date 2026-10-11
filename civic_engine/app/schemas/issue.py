"""Schemas for Civic Issue Extraction, Matching, and Intelligence."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import CivicCategory, VerificationStatus, IssueRelationshipType


class ExtractedIssueSchema(BaseModel):
    """
    Strict schema representing an individual civic issue extracted from source text.
    Used for AI output validation before database persistence.
    """
    issue_title: str = Field(..., description="Clear, concise title summarizing the civic problem")
    problem_description: str = Field(..., description="Concise description of the observed defect or civic issue")
    category: str = Field(..., description="Primary civic issue category")
    subcategory: Optional[str] = Field(default=None, description="Specific subcategory if applicable")
    location_mentioned: Optional[str] = Field(default=None, description="Exact location string as stated in source text")
    normalized_location: Optional[str] = Field(default=None, description="Normalized locality, landmark, or street name")
    latitude: Optional[float] = Field(default=None, description="Latitude only if reliably geocoded")
    longitude: Optional[float] = Field(default=None, description="Longitude only if reliably geocoded")
    affected_population: Optional[str] = Field(default="Inferred: Local residents and commuters", description="Estimated community or commuters impacted")
    first_reported_date: Optional[str] = Field(default=None, description="Date first observed if explicitly stated, ISO format or YYYY-MM-DD")
    most_recent_observation_date: Optional[str] = Field(default=None, description="Most recent observation date mentioned")
    possible_causes: List[str] = Field(default_factory=list, description="Reported or inferred causes")
    reported_consequences: List[str] = Field(default_factory=list, description="Immediate impact or hazard consequences")
    evidence_excerpts: List[str] = Field(default_factory=list, description="Direct verbatim quotes/excerpts from the source supporting this finding")
    source_references: List[str] = Field(default_factory=list, description="Identifiers, headlines, or URLs referencing the evidence")
    confidence_score: float = Field(default=0.75, ge=0.0, le=1.0, description="Confidence score of extraction")
    missing_information: List[str] = Field(default_factory=list, description="Critical missing facts (e.g., exact ward number, contractor name, depth)")
    verification_status: str = Field(default="UNVERIFIED", description="UNVERIFIED, COMMUNITY_REPORTED, CORROBORATED")
    suggested_next_steps: List[str] = Field(default_factory=list, description="Preliminary next steps to clarify or inspect")


class ExtractionBatchResult(BaseModel):
    """Container for batch extraction from a single source."""
    issues: List[ExtractedIssueSchema] = Field(default_factory=list)
    language_detected: str = "en"
    ai_provider_used: str
    ai_model_used: str
    processing_notes: Optional[str] = None


class ObservationResponse(BaseModel):
    """API response model for an individual observation."""
    id: str
    source_id: str
    consolidated_issue_id: Optional[str] = None
    issue_title: str
    problem_description: str
    category: str
    subcategory: Optional[str] = None
    location_mentioned: Optional[str] = None
    normalized_location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    affected_population: Optional[str] = None
    evidence_excerpts: List[str] = []
    missing_information: List[str] = []
    verification_status: str
    confidence_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConsolidatedIssueResponse(BaseModel):
    """API representation of a consolidated civic issue record."""
    id: str
    title: str
    summary: str
    category: str
    subcategory: Optional[str] = None
    normalized_location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    jurisdiction_name: Optional[str] = None
    ward_zone: Optional[str] = None
    observation_count: int
    distinct_publishers_count: int
    first_seen_date: Optional[datetime] = None
    last_seen_date: Optional[datetime] = None
    is_recurring: bool
    recurrence_pattern: str
    trend_direction: str
    verification_level: str
    composite_priority_score: float
    severity_score: float
    urgency_score: float
    recurrence_score: float
    evidence_strength_score: float
    community_impact_score: float
    actionability_score: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ConsolidatedIssueDetailResponse(ConsolidatedIssueResponse):
    """Detailed intelligence report and linked evidence for a consolidated issue."""
    what_is_happening: Optional[str] = None
    where_is_it_happening: Optional[str] = None
    unverified_information: List[str] = []
    affected_stakeholders_summary: Optional[str] = None
    recommended_practical_action: Optional[str] = None
    score_reasons: Dict[str, Any] = Field(default_factory=dict)
    observations: List[ObservationResponse] = []
    opportunities_count: int = 0
    stakeholders_count: int = 0


class ConsolidatedIssueListResponse(BaseModel):
    """Paginated collection of consolidated issues."""
    items: List[ConsolidatedIssueResponse]
    total: int
    page: int
    page_size: int


class RelatedIssueMatchSchema(BaseModel):
    """Schema representing an evaluated relationship between two issues."""
    target_issue_id: str
    target_title: str
    relationship_type: IssueRelationshipType
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    match_reasons: List[str] = Field(default_factory=list)


class IssueEvidenceItem(BaseModel):
    """Detailed evidence piece linking back to a source."""
    observation_id: str
    source_id: str
    source_title: str
    publisher: Optional[str] = None
    publication_date: Optional[datetime] = None
    source_url_or_ref: Optional[str] = None
    evidence_excerpts: List[str] = []
    possible_causes: List[str] = []
    reported_consequences: List[str] = []
    missing_information: List[str] = []
    confidence_score: float


class IssueEvidenceResponse(BaseModel):
    """Full evidentiary dossier for an issue."""
    issue_id: str
    issue_title: str
    distinct_sources_count: int
    evidence_items: List[IssueEvidenceItem]
    unverified_facts: List[str] = []
    corroboration_summary: str
