import logging
from typing import List, Dict, Any, Tuple
from uuid import UUID, uuid4
from datetime import datetime, date, timedelta

from ..config import get_settings
from ..database import get_repository
from ..models.schemas import (
    CivicCategory,
    SeverityLevel,
    EventStatus,
    SuggestedActionBlueprint,
    NGOVolunteerEventOut,
    AlertPayload,
)

logger = logging.getLogger("civic_pipeline.dispatcher")


class NGODispatcher:
    """
    Automates matching of verified civic issues (authenticity_score >= 65)
    with registered local NGOs by ward and category, pre-populating draft
    volunteer mobilization events and generating alert payloads.
    """

    def __init__(self):
        self.settings = get_settings()
        self.repo = get_repository()

    def dispatch_verified_issue(
        self,
        issue: Dict[str, Any],
        action_blueprint: Optional[SuggestedActionBlueprint] = None
    ) -> Tuple[List[Dict[str, Any]], List[AlertPayload]]:
        """
        Evaluates issue verification threshold, queries matching NGOs,
        creates draft volunteer mobilization events, and generates alert payloads.
        """
        authenticity_score = issue.get("authenticity_score", 0)
        issue_id = str(issue["id"])
        ward = issue.get("ward", "")
        category = issue.get("category", "")
        severity = issue.get("severity", "Medium")

        # Check minimum verification threshold (65)
        if authenticity_score < self.settings.VERIFICATION_THRESHOLD:
            logger.info(
                "Issue %s does not meet verification threshold (%d < %d). Skipping NGO dispatch.",
                issue_id, authenticity_score, self.settings.VERIFICATION_THRESHOLD
            )
            return [], []

        # Find registered NGOs matching both operating ward and primary causes
        matching_ngos = self.repo.find_matching_ngos(ward=ward, category=category)
        if not matching_ngos:
            logger.info("No matching registered NGOs found for ward '%s' and cause '%s'.", ward, category)
            return [], []

        logger.info("Found %d matching NGOs for verified issue %s in %s", len(matching_ngos), issue_id, ward)

        # Reconstruct or parse action blueprint
        blueprint = action_blueprint or self._extract_blueprint(issue)

        dispatched_events = []
        alert_payloads = []

        # Determine target volunteer count based on severity
        volunteer_target_map = {
            "Low": 10,
            "Medium": 20,
            "High": 35,
            "Critical": 50
        }
        target_volunteers = volunteer_target_map.get(severity, 20)

        # Default event date scheduled for upcoming Saturday
        event_date = self._get_next_event_date()
        meeting_point = f"Community Junction, {ward} (Coordinates: {issue.get('latitude')}, {issue.get('longitude')})"

        for ngo in matching_ngos:
            ngo_id = str(ngo["id"])
            ngo_name = ngo.get("name", "Local Civic Action NGO")

            # Check if a draft event already exists for this NGO and issue to prevent duplicates
            existing_events = [
                e for e in self.repo.get_events_by_issue(issue_id)
                if str(e.get("ngo_id")) == ngo_id
            ]

            if existing_events:
                event_record = existing_events[0]
            else:
                event_data = {
                    "id": str(uuid4()),
                    "issue_id": issue_id,
                    "ngo_id": ngo_id,
                    "event_title": blueprint.event_title or f"Volunteer Clean-Up & Remediation - {ward}",
                    "event_date": event_date.isoformat(),
                    "meeting_point": meeting_point,
                    "target_volunteers": target_volunteers,
                    "registered_volunteers": 0,
                    "required_gear": blueprint.required_gear,
                    "tasks_breakdown": blueprint.tasks_breakdown,
                    "safety_guidelines": blueprint.safety_guidelines,
                    "status": EventStatus.DRAFT.value,
                }
                event_record = self.repo.insert_event(event_data)

            dispatched_events.append(event_record)

            # Generate alert payload for the NGO dashboard
            alert = AlertPayload(
                ngo_id=UUID(ngo_id),
                ngo_name=ngo_name,
                issue_id=UUID(issue_id),
                issue_title=issue.get("title", "Civic Problem"),
                category=CivicCategory(category),
                ward=ward,
                severity=SeverityLevel(severity),
                authenticity_score=authenticity_score,
                evidence_summary=issue.get("summary", ""),
                prepackaged_event_id=UUID(event_record["id"]),
                suggested_action_blueprint=blueprint,
            )
            alert_payloads.append(alert)

        return dispatched_events, alert_payloads

    def _extract_blueprint(self, issue: Dict[str, Any]) -> SuggestedActionBlueprint:
        """Extract blueprint from issue metadata or build robust default."""
        bp_dict = issue.get("action_blueprint")
        if isinstance(bp_dict, dict) and bp_dict.get("event_title"):
            try:
                return SuggestedActionBlueprint(**bp_dict)
            except Exception:
                pass

        category = issue.get("category", "Sanitation")
        ward = issue.get("ward", "Local Ward")
        return SuggestedActionBlueprint(
            event_title=f"{category} Civic Action Drive - {ward}",
            required_gear=["Protective gloves", "High-visibility vests", "Trash grabbers / basic tools"],
            tasks_breakdown=[
                "Survey site perimeter and assemble volunteer teams",
                "Execute remediation tasks according to safety briefing",
                "Document completed cleanup and submit report"
            ],
            safety_guidelines=[
                "Wear all required protective equipment",
                "Never handle hazardous or sharp waste directly",
                "Maintain hydration and check in with group coordinator"
            ]
        )

    def _get_next_event_date(self) -> date:
        """Calculates next upcoming Saturday for default weekend civic mobilization."""
        today = date.today()
        # Saturday is weekday 5
        days_ahead = (5 - today.weekday()) % 7
        if days_ahead <= 1:
            days_ahead += 7  # ensure at least 2 days planning lead time
        return today + timedelta(days=days_ahead)


_dispatcher_instance = None


def get_ngo_dispatcher() -> NGODispatcher:
    """Retrieve singleton instance of NGODispatcher."""
    global _dispatcher_instance
    if _dispatcher_instance is None:
        _dispatcher_instance = NGODispatcher()
    return _dispatcher_instance
