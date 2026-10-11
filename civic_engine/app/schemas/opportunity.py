"""Schemas for Civic Action Opportunities, Reviews, and Prioritization."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import ActivityType, OpportunityReviewStatus


class CivicActionPlanSchema(BaseModel):
    """Structured AI output schema for generating a civic action opportunity."""
    title: str = Field(..., description="Actionable, inspiring title for the civic opportunity")
    problem_summary: str = Field(..., description="Concise summary of the civic problem being addressed")
    why_needed: str = Field(..., description="Compelling rationale for community or citizen involvement")
    activity_type: ActivityType = Field(..., description="Type of civic activity")
    step_by_step_plan: List[str] = Field(..., description="Clear, numbered chronological action steps")
    intended_beneficiaries: str = Field(..., description="Primary beneficiaries (pedestrians, residents, school children)")
    suggested_roles: List[str] = Field(..., description="Suggested volunteer roles, e.g., 'Photo Auditor', 'Survey Coordinator'")
    required_materials: List[str] = Field(default_factory=list, description="Safe materials, e.g., 'Smartphones', 'Clipboard', 'Reflective Vests'")
    estimated_effort_hours: float = Field(default=2.0, ge=0.5, le=100.0, description="Estimated effort in hours (clearly labeled as estimate)")
    suggested_participant_count: int = Field(default=5, ge=1, le=500, description="Ideal number of volunteer participants")
    potential_collaborators: List[str] = Field(default_factory=list, description="NGOs, RWAs, student groups, or community clubs")
    escalation_channel: str = Field(..., description="Official grievance portal, ward helpline, or municipal department")
    expected_outcomes: str = Field(..., description="Measurable outcome expected upon completion")
    success_metrics: str = Field(..., description="Criteria for assessing success, e.g., '100% potholes logged with GPS'")
    safety_considerations: List[str] = Field(..., description="Critical safety guidelines and hazards to avoid")
    prerequisites_and_permissions: List[str] = Field(default_factory=list, description="Permissions required from authorities before action")
    is_official_authorization_required: bool = Field(default=False, description="True if activity cannot proceed without municipal permit")
    safety_risk_level: str = Field(default="LOW", description="LOW, MODERATE, HIGH_REQUIRES_AUTHORITY")
    ai_confidence: float = Field(default=0.85, ge=0.0, le=1.0)


class CivicOpportunityResponse(BaseModel):
    """API representation of a Civic Action Opportunity."""
    id: str
    issue_id: str
    issue_title: Optional[str] = None
    title: str
    problem_summary: str
    why_needed: str
    activity_type: str
    step_by_step_plan: List[str] = []
    intended_beneficiaries: Optional[str] = None
    suggested_roles: List[str] = []
    required_materials: List[str] = []
    estimated_effort_hours: float
    suggested_participant_count: int
    potential_collaborators: List[str] = []
    escalation_channel: Optional[str] = None
    expected_outcomes: Optional[str] = None
    success_metrics: Optional[str] = None
    safety_considerations: List[str] = []
    prerequisites_and_permissions: List[str] = []
    is_official_authorization_required: bool
    safety_risk_level: str
    ai_confidence: float
    review_status: str
    review_notes: Optional[str] = None
    priority_score: float
    priority_breakdown: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CivicOpportunityListResponse(BaseModel):
    """Paginated collection of civic opportunities."""
    items: List[CivicOpportunityResponse]
    total: int
    page: int
    page_size: int


class OpportunityReviewRequest(BaseModel):
    """Submission payload for human review of an opportunity."""
    reviewer_name: str = Field(..., min_length=2, max_length=100)
    status: OpportunityReviewStatus = Field(..., description="APPROVED, REJECTED, MODIFIED")
    feedback_comments: Optional[str] = Field(default=None, description="Detailed review comments")
    modifications: Optional[Dict[str, Any]] = Field(default=None, description="Field overrides if modified")


class OpportunityReviewResponse(BaseModel):
    """Audit response of completed opportunity review."""
    id: str
    opportunity_id: str
    reviewer_name: str
    status: str
    feedback_comments: Optional[str] = None
    reviewed_at: datetime

    model_config = ConfigDict(from_attributes=True)
