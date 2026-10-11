"""Schemas for Civic Analytics and Trends reporting."""

from typing import List, Dict, Any
from pydantic import BaseModel


class CategoryCount(BaseModel):
    category: str
    issues_count: int
    observations_count: int
    avg_priority_score: float


class CategoryAnalyticsResponse(BaseModel):
    total_issues: int
    categories: List[CategoryCount]


class TrendItem(BaseModel):
    trend_direction: str
    count: int
    recurrence_patterns: Dict[str, int]


class TrendAnalyticsResponse(BaseModel):
    total_issues: int
    recurring_issues_count: int
    trends: List[TrendItem]
    recent_activity: List[Dict[str, Any]]


class LocationItem(BaseModel):
    location: str
    jurisdiction_name: str
    ward_zone: str
    issues_count: int
    avg_severity: float
    coordinates: Dict[str, float]


class LocationAnalyticsResponse(BaseModel):
    locations: List[LocationItem]
    top_hotspots: List[str]


class OpportunityAnalyticsResponse(BaseModel):
    total_opportunities: int
    by_status: Dict[str, int]
    by_activity_type: Dict[str, int]
    by_safety_level: Dict[str, int]
    total_estimated_volunteer_hours: float
    avg_priority_score: float
