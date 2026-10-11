import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter

from ..database import get_repository
from ..models.schemas import (
    PublicMapClusterOut,
    PublicEventSummary,
    CivicCategory,
    SeverityLevel,
    IssueStatus,
    EventStatus,
)

logger = logging.getLogger("civic_pipeline.routes.public")
router = APIRouter(prefix="/api/public", tags=["Public Map & Citizen Interface"])


@router.get(
    "/map-clusters",
    response_model=List[PublicMapClusterOut],
    summary="Get all verified civic issues with active volunteer mobilization events for map visualization"
)
async def get_public_map_clusters() -> List[PublicMapClusterOut]:
    """
    Returns verified civic issues that have active/published citizen volunteer mobilization events.
    Enables interactive frontend map rendering with pin clusters, issue details, coordinates,
    and associated NGO RSVP drives.
    """
    repo = get_repository()
    cluster_records = repo.get_all_active_map_clusters()

    results: List[PublicMapClusterOut] = []
    for item in cluster_records:
        events = item.get("active_events", [])
        mapped_events = [
            PublicEventSummary(
                event_id=UUID(e["event_id"]),
                ngo_id=UUID(e["ngo_id"]),
                ngo_name=e.get("ngo_name", "Local Civic Action NGO"),
                event_title=e["event_title"],
                event_date=e["event_date"],
                meeting_point=e["meeting_point"],
                target_volunteers=e["target_volunteers"],
                registered_volunteers=e.get("registered_volunteers", 0),
                required_gear=e.get("required_gear", []),
                tasks_breakdown=e.get("tasks_breakdown", []),
                safety_guidelines=e.get("safety_guidelines", []),
                status=EventStatus(e["status"])
            )
            for e in events
        ]

        results.append(
            PublicMapClusterOut(
                issue_id=UUID(item["id"]),
                title=item["title"],
                summary=item["summary"],
                category=CivicCategory(item["category"]),
                ward=item["ward"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                severity=SeverityLevel(item["severity"]),
                authenticity_score=item["authenticity_score"],
                responsible_authority=item["responsible_authority"],
                source_count=item.get("source_count", 1),
                status=IssueStatus(item["status"]),
                active_events=mapped_events
            )
        )

    return results
