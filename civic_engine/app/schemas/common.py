"""Common enums and base schema definitions for the Civic Engine."""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class CivicCategory(str, Enum):
    ROADS_AND_POTHOLES = "Roads and potholes"
    TRAFFIC_AND_ROAD_SAFETY = "Traffic congestion and road safety"
    WATER_SUPPLY_AND_QUALITY = "Water supply and water quality"
    DRAINAGE_AND_WATERLOGGING = "Drainage and waterlogging"
    WASTE_MANAGEMENT = "Waste management"
    AIR_AND_NOISE_POLLUTION = "Air and noise pollution"
    PUBLIC_HEALTH_AND_SANITATION = "Public health and sanitation"
    PUBLIC_INFRASTRUCTURE = "Public infrastructure"
    STREETLIGHTS_AND_ELECTRICITY = "Streetlights and electricity infrastructure"
    PUBLIC_TRANSPORT = "Public transport"
    ENVIRONMENTAL_DEGRADATION = "Environmental degradation"
    PUBLIC_ACCESSIBILITY = "Public accessibility"
    EDUCATION_INFRASTRUCTURE = "Education infrastructure"
    PUBLIC_SERVICE_DELIVERY = "Public-service delivery"
    OTHER_EMERGING_CONCERNS = "Other emerging civic concerns"


CIVIC_CATEGORIES_LIST: List[str] = [c.value for c in CivicCategory]


class SourceType(str, Enum):
    RSS = "rss"
    NEWS_WEB = "news_web"
    GOV_DOC = "gov_doc"
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"
    USER_TEXT = "user_text"
    IMAGE = "image"


class ProcessingStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DUPLICATE = "DUPLICATE"


class VerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    COMMUNITY_REPORTED = "COMMUNITY_REPORTED"
    CORROBORATED = "CORROBORATED"
    OFFICIALLY_ACKNOWLEDGED = "OFFICIALLY_ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


class IssueRelationshipType(str, Enum):
    DUPLICATE_REPORT = "DUPLICATE_REPORT"
    RECURRING_INCIDENT = "RECURRING_INCIDENT"
    NEARBY_SIMILAR = "NEARBY_SIMILAR"
    CROSS_AREA_SIMILAR = "CROSS_AREA_SIMILAR"
    UNRELATED_KEYWORD_MATCH = "UNRELATED_KEYWORD_MATCH"


class OpportunityReviewStatus(str, Enum):
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MODIFIED = "MODIFIED"


class ActivityType(str, Enum):
    EVIDENCE_COLLECTION = "EVIDENCE_COLLECTION"
    COMMUNITY_SURVEY = "COMMUNITY_SURVEY"
    OFFICIAL_GRIEVANCE_FILING = "OFFICIAL_GRIEVANCE_FILING"
    AWARENESS_CAMPAIGN = "AWARENESS_CAMPAIGN"
    AUTHORIZED_CLEANUP = "AUTHORIZED_CLEANUP"
    ACCESSIBILITY_AUDIT = "ACCESSIBILITY_AUDIT"
    PROGRESS_MONITORING = "PROGRESS_MONITORING"
