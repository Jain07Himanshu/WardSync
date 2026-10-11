"""Schemas for Stakeholder Discovery and Jurisdiction Mapping."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class StakeholderResponse(BaseModel):
    """Details of a registered civic authority, ward office, or NGO."""
    id: str
    name: str
    department: Optional[str] = None
    jurisdiction_level: str
    jurisdiction_area: str
    official_website: Optional[str] = None
    public_portal_url: Optional[str] = None
    public_helpline: Optional[str] = None
    public_email: Optional[str] = None
    grievance_redressal_mechanism: Optional[str] = None
    is_verified_in_registry: bool

    model_config = ConfigDict(from_attributes=True)


class IssueStakeholderResponse(BaseModel):
    """An authority/stakeholder mapped to a specific civic issue."""
    id: str
    issue_id: str
    stakeholder_id: Optional[str] = None
    candidate_name: str
    department: Optional[str] = None
    relevance_reason: str
    jurisdiction_coverage: Optional[str] = None
    official_website: Optional[str] = None
    public_portal_url: Optional[str] = None
    public_helpline: Optional[str] = None
    public_email: Optional[str] = None
    grievance_redressal_mechanism: Optional[str] = None
    verification_status: str
    confidence_level: float
    source_reference: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StakeholderRecommendationSchema(BaseModel):
    """Strict AI recommendation schema for identifying authorities."""
    organization_name: str = Field(..., description="Name of the department, civic body, or community initiative")
    department: Optional[str] = Field(default=None, description="Specific department within civic body")
    relevance_reason: str = Field(..., description="Explain why this entity is accountable or able to assist")
    jurisdiction_area: Optional[str] = Field(default=None, description="Geographic jurisdiction or ward coverage")
    verification_status: str = Field(default="CANDIDATE_UNVERIFIED", description="VERIFIED_REGISTRY or CANDIDATE_UNVERIFIED")
    confidence_level: float = Field(default=0.6, ge=0.0, le=1.0)
    source_reference: Optional[str] = Field(default=None, description="Document or guideline where authority is derived")
    public_portal_or_contact_hint: Optional[str] = Field(default=None, description="Safe reference to official public portal name, without inventing URLs")


class StakeholderDiscoveryResult(BaseModel):
    """Response containing discovered stakeholders for an issue."""
    issue_id: str
    issue_title: str
    stakeholders: List[IssueStakeholderResponse]
    jurisdiction_matched: Optional[str] = None
    verification_notice: str
