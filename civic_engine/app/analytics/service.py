"""Analytics service for aggregating civic insights and reporting."""

from typing import Dict, Any, List
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import (
    ConsolidatedIssue,
    ExtractedIssueObservation,
    CivicOpportunity,
)
from app.schemas.analytics import (
    CategoryAnalyticsResponse,
    CategoryCount,
    TrendAnalyticsResponse,
    TrendItem,
    LocationAnalyticsResponse,
    LocationItem,
    OpportunityAnalyticsResponse,
)


class AnalyticsService:
    """Computes real-time summaries and aggregate metrics across issues and actions."""

    def __init__(self, db: Session):
        self.db = db

    def get_category_analytics(self) -> CategoryAnalyticsResponse:
        total_issues = self.db.query(ConsolidatedIssue).count()
        category_rows = (
            self.db.query(
                ConsolidatedIssue.category,
                func.count(ConsolidatedIssue.id).label("issue_count"),
                func.sum(ConsolidatedIssue.observation_count).label("obs_count"),
                func.avg(ConsolidatedIssue.composite_priority_score).label("avg_priority"),
            )
            .group_by(ConsolidatedIssue.category)
            .all()
        )

        categories = []
        for cat, count, obs, avg_p in category_rows:
            categories.append(
                CategoryCount(
                    category=cat,
                    issues_count=count,
                    observations_count=int(obs or count),
                    avg_priority_score=round(float(avg_p or 50.0), 1),
                )
            )

        return CategoryAnalyticsResponse(total_issues=total_issues, categories=categories)

    def get_trend_analytics(self) -> TrendAnalyticsResponse:
        total_issues = self.db.query(ConsolidatedIssue).count()
        recurring_count = self.db.query(ConsolidatedIssue).filter(ConsolidatedIssue.is_recurring.is_(True)).count()

        trend_rows = (
            self.db.query(
                ConsolidatedIssue.trend_direction,
                func.count(ConsolidatedIssue.id)
            )
            .group_by(ConsolidatedIssue.trend_direction)
            .all()
        )

        trends = []
        for direction, count in trend_rows:
            patterns = (
                self.db.query(
                    ConsolidatedIssue.recurrence_pattern,
                    func.count(ConsolidatedIssue.id)
                )
                .filter(ConsolidatedIssue.trend_direction == direction)
                .group_by(ConsolidatedIssue.recurrence_pattern)
                .all()
            )
            trends.append(
                TrendItem(
                    trend_direction=direction,
                    count=count,
                    recurrence_patterns={p: c for p, c in patterns},
                )
            )

        # Recent activities
        recent = (
            self.db.query(ConsolidatedIssue)
            .order_by(ConsolidatedIssue.updated_at.desc())
            .limit(5)
            .all()
        )
        recent_activity = [
            {
                "id": i.id,
                "title": i.title,
                "category": i.category,
                "location": i.normalized_location,
                "updated_at": i.updated_at.isoformat() if i.updated_at else None,
            }
            for i in recent
        ]

        return TrendAnalyticsResponse(
            total_issues=total_issues,
            recurring_issues_count=recurring_count,
            trends=trends,
            recent_activity=recent_activity,
        )

    def get_location_analytics(self) -> LocationAnalyticsResponse:
        loc_rows = (
            self.db.query(
                ConsolidatedIssue.normalized_location,
                ConsolidatedIssue.jurisdiction_name,
                ConsolidatedIssue.ward_zone,
                func.count(ConsolidatedIssue.id).label("issue_count"),
                func.avg(ConsolidatedIssue.severity_score).label("avg_sev"),
                func.avg(ConsolidatedIssue.latitude).label("avg_lat"),
                func.avg(ConsolidatedIssue.longitude).label("avg_lon"),
            )
            .filter(ConsolidatedIssue.normalized_location.isnot(None))
            .group_by(
                ConsolidatedIssue.normalized_location,
                ConsolidatedIssue.jurisdiction_name,
                ConsolidatedIssue.ward_zone,
            )
            .all()
        )

        locations = []
        hotspots = []
        for loc, jur, ward, count, avg_sev, lat, lon in loc_rows:
            locations.append(
                LocationItem(
                    location=loc or "Unknown",
                    jurisdiction_name=jur or "Municipal Authority",
                    ward_zone=ward or "General",
                    issues_count=count,
                    avg_severity=round(float(avg_sev or 5.0), 1),
                    coordinates={"latitude": float(lat or 19.0760), "longitude": float(lon or 72.8777)},
                )
            )
            if count >= 2:
                hotspots.append(loc)

        return LocationAnalyticsResponse(locations=locations, top_hotspots=hotspots)

    def get_opportunity_analytics(self) -> OpportunityAnalyticsResponse:
        total = self.db.query(CivicOpportunity).count()

        status_rows = self.db.query(CivicOpportunity.review_status, func.count(CivicOpportunity.id)).group_by(CivicOpportunity.review_status).all()
        act_rows = self.db.query(CivicOpportunity.activity_type, func.count(CivicOpportunity.id)).group_by(CivicOpportunity.activity_type).all()
        safety_rows = self.db.query(CivicOpportunity.safety_risk_level, func.count(CivicOpportunity.id)).group_by(CivicOpportunity.safety_risk_level).all()

        total_hours = self.db.query(func.sum(CivicOpportunity.estimated_effort_hours)).scalar() or 0.0
        avg_priority = self.db.query(func.avg(CivicOpportunity.priority_score)).scalar() or 50.0

        return OpportunityAnalyticsResponse(
            total_opportunities=total,
            by_status={s: c for s, c in status_rows},
            by_activity_type={a: c for a, c in act_rows},
            by_safety_level={r: c for r, c in safety_rows},
            total_estimated_volunteer_hours=round(float(total_hours), 1),
            avg_priority_score=round(float(avg_priority), 1),
        )
