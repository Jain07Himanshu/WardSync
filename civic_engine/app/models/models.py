"""SQLAlchemy models for Civic Issue Discovery & Action Engine."""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Float,
    Integer,
    Boolean,
    ForeignKey,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


def generate_uuid() -> str:
    """Generate a random UUID4 string."""
    return str(uuid.uuid4())


class Source(Base):
    """Normalized ingested public or user-uploaded source record."""
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_type = Column(String(50), nullable=False, index=True)  # rss, news_web, gov_doc, pdf, docx, csv, user_text
    original_title = Column(String(500), nullable=False)
    original_url_or_ref = Column(String(1000), nullable=True)
    publisher = Column(String(255), nullable=True, index=True)
    publication_date = Column(DateTime, nullable=True)
    retrieval_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    extracted_text = Column(Text, nullable=False)
    language = Column(String(10), default="en", nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)
    processing_status = Column(String(50), default="PENDING", index=True)  # PENDING, PROCESSING, COMPLETED, FAILED, DUPLICATE
    error_message = Column(Text, nullable=True)
    metadata_payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    observations = relationship("ExtractedIssueObservation", back_populates="source", cascade="all, delete-orphan")


class SourceProcessingJob(Base):
    """Track asynchronous background ingestion and AI pipeline jobs."""
    __tablename__ = "source_processing_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    job_type = Column(String(50), nullable=False)  # INGESTION, EXTRACTION, MATCHING, FULL_PIPELINE
    status = Column(String(50), default="PENDING", index=True)  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=True)
    issue_id = Column(String(36), nullable=True)
    progress_percentage = Column(Integer, default=0)
    total_items = Column(Integer, default=0)
    processed_items = Column(Integer, default=0)
    error_details = Column(Text, nullable=True)
    result_summary = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class ExtractedIssueObservation(Base):
    """An individual civic issue observation extracted from a single source."""
    __tablename__ = "extracted_issue_observations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=False, index=True)
    consolidated_issue_id = Column(String(36), ForeignKey("consolidated_issues.id"), nullable=True, index=True)

    issue_title = Column(String(500), nullable=False)
    problem_description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True)
    location_mentioned = Column(String(500), nullable=True)
    normalized_location = Column(String(500), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    affected_population = Column(String(255), nullable=True)
    first_reported_date = Column(DateTime, nullable=True)
    most_recent_observation_date = Column(DateTime, nullable=True)
    possible_causes = Column(JSON, default=list)
    reported_consequences = Column(JSON, default=list)
    evidence_excerpts = Column(JSON, default=list)
    missing_information = Column(JSON, default=list)
    verification_status = Column(String(50), default="UNVERIFIED", index=True)
    confidence_score = Column(Float, default=0.5)
    language = Column(String(10), default="en")
    suggested_next_steps = Column(JSON, default=list)

    # Provenance and AI model tracking
    ai_provider = Column(String(50), nullable=True)
    ai_model = Column(String(100), nullable=True)
    raw_ai_response = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    source = relationship("Source", back_populates="observations")
    consolidated_issue = relationship("ConsolidatedIssue", back_populates="observations")


class ConsolidatedIssue(Base):
    """A consolidated, deduplicated civic problem linked to multiple observations."""
    __tablename__ = "consolidated_issues"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True)
    normalized_location = Column(String(500), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    jurisdiction_name = Column(String(255), nullable=True, index=True)
    ward_zone = Column(String(100), nullable=True, index=True)

    observation_count = Column(Integer, default=1)
    distinct_publishers_count = Column(Integer, default=1)
    first_seen_date = Column(DateTime, nullable=True)
    last_seen_date = Column(DateTime, nullable=True)

    # Recurrence & Trend intelligence
    is_recurring = Column(Boolean, default=False, index=True)
    recurrence_pattern = Column(String(50), default="SINGLE_INCIDENT")  # SINGLE_INCIDENT, RECURRING_CHRONIC, SEASONAL_MONSOON, EXPANDING_CORRIDOR
    trend_direction = Column(String(50), default="NEW")  # NEW, STABLE, ESCALATING, DECREASING, RESOLVED
    verification_level = Column(String(50), default="SINGLE_UNVERIFIED")  # SINGLE_UNVERIFIED, CROSS_SOURCE_CORROBORATED, OFFICIALLY_NOTIFIED

    # Explainable Scoring (1.0 to 10.0 scale, composite 0-100)
    severity_score = Column(Float, default=5.0)
    urgency_score = Column(Float, default=5.0)
    recurrence_score = Column(Float, default=1.0)
    evidence_strength_score = Column(Float, default=5.0)
    community_impact_score = Column(Float, default=5.0)
    actionability_score = Column(Float, default=5.0)
    composite_priority_score = Column(Float, default=50.0, index=True)
    score_reasons = Column(JSON, default=dict)

    # Intelligence & Context Report
    what_is_happening = Column(Text, nullable=True)
    where_is_it_happening = Column(Text, nullable=True)
    unverified_information = Column(JSON, default=list)
    affected_stakeholders_summary = Column(Text, nullable=True)
    recommended_practical_action = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    observations = relationship("ExtractedIssueObservation", back_populates="consolidated_issue")
    stakeholders = relationship("IssueStakeholderMapping", back_populates="issue", cascade="all, delete-orphan")
    opportunities = relationship("CivicOpportunity", back_populates="issue", cascade="all, delete-orphan")


class IssueRelationship(Base):
    """Cross-issue links with typed relationship taxonomy."""
    __tablename__ = "issue_relationships"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_issue_id = Column(String(36), ForeignKey("consolidated_issues.id"), nullable=False, index=True)
    target_issue_id = Column(String(36), ForeignKey("consolidated_issues.id"), nullable=False, index=True)
    relationship_type = Column(String(50), nullable=False, index=True)  # DUPLICATE_REPORT, RECURRING_INCIDENT, NEARBY_SIMILAR, CROSS_AREA_SIMILAR, UNRELATED_KEYWORD_MATCH
    similarity_score = Column(Float, default=0.0)
    match_reasons = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class Stakeholder(Base):
    """Verified directory of civic authorities, ward offices, and public NGOs."""
    __tablename__ = "stakeholders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    department = Column(String(255), nullable=True)
    jurisdiction_level = Column(String(50), nullable=False)  # WARD, MUNICIPAL, DISTRICT, STATE, NATIONAL, NGO_COMMUNITY
    jurisdiction_area = Column(String(255), nullable=False, index=True)
    categories_handled = Column(JSON, default=list)
    official_website = Column(String(500), nullable=True)
    public_portal_url = Column(String(500), nullable=True)
    public_helpline = Column(String(100), nullable=True)
    public_email = Column(String(255), nullable=True)
    grievance_redressal_mechanism = Column(String(500), nullable=True)
    is_verified_in_registry = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class IssueStakeholderMapping(Base):
    """Link between a civic issue and a candidate/verified authority or NGO."""
    __tablename__ = "issue_stakeholder_mappings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    issue_id = Column(String(36), ForeignKey("consolidated_issues.id"), nullable=False, index=True)
    stakeholder_id = Column(String(36), ForeignKey("stakeholders.id"), nullable=True)
    candidate_name = Column(String(255), nullable=False)
    relevance_reason = Column(Text, nullable=False)
    jurisdiction_coverage = Column(String(255), nullable=True)
    verification_status = Column(String(50), default="CANDIDATE_UNVERIFIED", index=True)  # VERIFIED_REGISTRY, CANDIDATE_UNVERIFIED
    confidence_level = Column(Float, default=0.5)
    source_reference = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    issue = relationship("ConsolidatedIssue", back_populates="stakeholders")
    stakeholder = relationship("Stakeholder")


class CivicOpportunity(Base):
    """Generated practical volunteer and citizen participation opportunity."""
    __tablename__ = "civic_opportunities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    issue_id = Column(String(36), ForeignKey("consolidated_issues.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    problem_summary = Column(Text, nullable=False)
    why_needed = Column(Text, nullable=False)
    activity_type = Column(String(100), nullable=False, index=True)
    step_by_step_plan = Column(JSON, default=list)
    intended_beneficiaries = Column(Text, nullable=True)
    suggested_roles = Column(JSON, default=list)
    required_materials = Column(JSON, default=list)
    estimated_effort_hours = Column(Float, default=2.0)
    suggested_participant_count = Column(Integer, default=5)
    potential_collaborators = Column(JSON, default=list)
    escalation_channel = Column(String(500), nullable=True)
    expected_outcomes = Column(Text, nullable=True)
    success_metrics = Column(Text, nullable=True)
    safety_considerations = Column(JSON, default=list)
    prerequisites_and_permissions = Column(JSON, default=list)
    is_official_authorization_required = Column(Boolean, default=False)
    safety_risk_level = Column(String(50), default="LOW")  # LOW, MODERATE, HIGH_REQUIRES_AUTHORITY

    ai_confidence = Column(Float, default=0.8)
    review_status = Column(String(50), default="PENDING_REVIEW", index=True)  # PENDING_REVIEW, APPROVED, REJECTED, MODIFIED
    review_notes = Column(Text, nullable=True)

    priority_score = Column(Float, default=50.0, index=True)
    priority_breakdown = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    issue = relationship("ConsolidatedIssue", back_populates="opportunities")
    reviews = relationship("OpportunityReview", back_populates="opportunity", cascade="all, delete-orphan")


class OpportunityReview(Base):
    """Review and audit decisions by humans on civic opportunities."""
    __tablename__ = "opportunity_reviews"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    opportunity_id = Column(String(36), ForeignKey("civic_opportunities.id"), nullable=False, index=True)
    reviewer_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # APPROVED, REJECTED, MODIFIED
    feedback_comments = Column(Text, nullable=True)
    modifications = Column(JSON, default=dict)
    reviewed_at = Column(DateTime, default=datetime.utcnow)

    opportunity = relationship("CivicOpportunity", back_populates="reviews")


class AuditEvent(Base):
    """Immutable audit trail of pipeline actions and AI outputs."""
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_type = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(36), nullable=False, index=True)
    ai_provider = Column(String(50), nullable=True)
    ai_model = Column(String(100), nullable=True)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


# Composite indexes for high performance query resolution
Index("ix_obs_source_category", ExtractedIssueObservation.source_id, ExtractedIssueObservation.category)
Index("ix_cons_category_loc", ConsolidatedIssue.category, ConsolidatedIssue.normalized_location)
Index("ix_rel_source_target", IssueRelationship.source_issue_id, IssueRelationship.target_issue_id)
