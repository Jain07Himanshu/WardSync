import logging
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from ..database import get_repository
from ..models.schemas import (
    EventPublishRequest,
    NGOVolunteerEventOut,
    EventStatus,
    IssueStatus,
)

logger = logging.getLogger("civic_pipeline.routes.events")
router = APIRouter(prefix="/api/events", tags=["Volunteer Mobilization Events"])


@router.post(
    "/publish",
    response_model=NGOVolunteerEventOut,
    summary="Accept and publish an AI-generated volunteer event blueprint live for citizen RSVP"
)
async def publish_volunteer_event(payload: EventPublishRequest) -> NGOVolunteerEventOut:
    """
    Enables an NGO administrator to accept an AI-generated mobilization draft,
    optionally customize event title, schedule date, meeting point, target headcount,
    gear requirements, tasks breakdown, and safety guidelines, and publish it live.

    Updating to 'published':
    1. Sets event status to 'published' so citizens can discover and RSVP.
    2. Updates the associated civic issue status to 'event_active'.
    """
    repo = get_repository()
    event_id_str = str(payload.event_id)
    ngo_id_str = str(payload.ngo_id)

    # 1. Fetch Event
    event = repo.get_event(event_id_str)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Volunteer event draft with ID '{payload.event_id}' not found."
        )

    # 2. Authorization / ownership check
    if str(event.get("ngo_id")) != ngo_id_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: This event draft does not belong to the requesting NGO."
        )

    # 3. Verify NGO status
    ngo = repo.get_ngo(ngo_id_str)
    if not ngo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NGO with ID '{payload.ngo_id}' not found."
        )

    # 4. Prepare updates
    updates = {"status": EventStatus.PUBLISHED.value}
    if payload.event_title:
        updates["event_title"] = payload.event_title
    if payload.event_date:
        updates["event_date"] = payload.event_date.isoformat()
    if payload.meeting_point:
        updates["meeting_point"] = payload.meeting_point
    if payload.target_volunteers is not None:
        updates["target_volunteers"] = payload.target_volunteers
    if payload.required_gear is not None:
        updates["required_gear"] = payload.required_gear
    if payload.tasks_breakdown is not None:
        updates["tasks_breakdown"] = payload.tasks_breakdown
    if payload.safety_guidelines is not None:
        updates["safety_guidelines"] = payload.safety_guidelines

    updated_event = repo.update_event(event_id_str, updates)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update event status."
        )

    # 5. Transition corresponding civic issue to 'event_active'
    issue_id_str = str(event["issue_id"])
    repo.update_issue(issue_id_str, {"status": IssueStatus.EVENT_ACTIVE.value})

    logger.info("Successfully published mobilization event %s for issue %s", event_id_str, issue_id_str)

    return NGOVolunteerEventOut(
        id=UUID(updated_event["id"]),
        issue_id=UUID(updated_event["issue_id"]),
        ngo_id=UUID(updated_event["ngo_id"]),
        event_title=updated_event["event_title"],
        event_date=updated_event["event_date"],
        meeting_point=updated_event["meeting_point"],
        target_volunteers=updated_event["target_volunteers"],
        registered_volunteers=updated_event.get("registered_volunteers", 0),
        required_gear=updated_event.get("required_gear", []),
        tasks_breakdown=updated_event.get("tasks_breakdown", []),
        safety_guidelines=updated_event.get("safety_guidelines", []),
        status=updated_event["status"],
        created_at=updated_event.get("created_at"),
        updated_at=updated_event.get("updated_at")
    )
