"""Analytics endpoints exposing civic trends, hot spots, and volunteer metrics."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import (
    CategoryAnalyticsResponse,
    TrendAnalyticsResponse,
    LocationAnalyticsResponse,
    OpportunityAnalyticsResponse,
)
from app.analytics.service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/categories", response_model=CategoryAnalyticsResponse, summary="Issue category analytics")
def get_categories_analytics(db: Session = Depends(get_db)):
    """Aggregate issue counts, observation volume, and average priority per civic category."""
    service = AnalyticsService(db)
    return service.get_category_analytics()


@router.get("/trends", response_model=TrendAnalyticsResponse, summary="Temporal trends and recurrence analysis")
def get_trends_analytics(db: Session = Depends(get_db)):
    """Analyze recurrence trends (chronic, seasonal, escalating) across all issues."""
    service = AnalyticsService(db)
    return service.get_trend_analytics()


@router.get("/locations", response_model=LocationAnalyticsResponse, summary="Geographic distribution and hotspots")
def get_locations_analytics(db: Session = Depends(get_db)):
    """Expose spatial distribution of issues across wards and pinpoint high-severity civic hotspots."""
    service = AnalyticsService(db)
    return service.get_location_analytics()


@router.get("/opportunities", response_model=OpportunityAnalyticsResponse, summary="Volunteer opportunity metrics")
def get_opportunities_analytics(db: Session = Depends(get_db)):
    """Expose metrics on generated civic actions, review statuses, and total estimated volunteer hours."""
    service = AnalyticsService(db)
    return service.get_opportunity_analytics()
