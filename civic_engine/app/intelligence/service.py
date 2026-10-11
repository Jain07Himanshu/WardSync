"""Civic Intelligence and Context Engine for explainable multi-factor scoring and analysis."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models.models import ConsolidatedIssue, ExtractedIssueObservation, Source
from app.providers.factory import get_ai_provider

logger = logging.getLogger(__name__)


class IntelligenceService:
    """Computes evidence-grounded civic intelligence reports and explainable multi-factor scores."""

    def __init__(self, db: Session, ai_provider_override: Optional[str] = None):
        self.db = db
        self.provider = get_ai_provider(provider_name=ai_provider_override)

    def analyze_consolidated_issue(self, issue_id: str) -> ConsolidatedIssue:
        """
        Evaluate full evidentiary context, compute explainable scores,
        and generate structured intelligence report.
        """
        issue = self.db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
        if not issue:
            raise ValueError(f"ConsolidatedIssue {issue_id} not found.")

        observations = self.db.query(ExtractedIssueObservation).filter(
            ExtractedIssueObservation.consolidated_issue_id == issue.id
        ).all()

        distinct_publishers = set()
        all_evidence = []
        all_missing = []
        all_causes = []
        all_consequences = []

        for obs in observations:
            source = self.db.query(Source).filter(Source.id == obs.source_id).first()
            if source and source.publisher:
                distinct_publishers.add(source.publisher)
            all_evidence.extend(obs.evidence_excerpts or [])
            all_missing.extend(obs.missing_information or [])
            all_causes.extend(obs.possible_causes or [])
            all_consequences.extend(obs.reported_consequences or [])

        distinct_source_count = max(1, len(distinct_publishers))
        issue.distinct_publishers_count = distinct_source_count
        issue.observation_count = len(observations)

        # 1. Evidence strength score (1.0 to 10.0)
        # Grounded strictly in distinct publisher corroboration and evidence quote counts
        evidence_score = min(10.0, 3.0 + (distinct_source_count * 2.0) + min(3.0, len(all_evidence) * 0.5))

        # 2. Recurrence score (1.0 to 10.0)
        recurrence_score = 1.0
        time_span_days = 0
        if issue.first_seen_date and issue.last_seen_date:
            time_span_days = max(0, (issue.last_seen_date - issue.first_seen_date).days)

        if issue.is_recurring or time_span_days > 14:
            issue.is_recurring = True
            recurrence_score = min(10.0, 5.0 + min(5.0, time_span_days / 7.0))
            issue.recurrence_pattern = "RECURRING_CHRONIC"
            issue.trend_direction = "ESCALATING" if len(observations) >= 3 else "STABLE"
        elif len(observations) > 1 and distinct_source_count > 1:
            # Multiple reports about same acute incident
            recurrence_score = 3.0
            issue.recurrence_pattern = "SINGLE_INCIDENT"
            issue.trend_direction = "NEW"
        else:
            recurrence_score = 1.0
            issue.recurrence_pattern = "SINGLE_INCIDENT"
            issue.trend_direction = "NEW"

        # 3. Severity & Urgency based on category and reported consequences
        cat_lower = (issue.category or "").lower()
        if "water supply" in cat_lower or "drainage" in cat_lower:
            severity = 8.0
            urgency = 7.5
        elif "roads" in cat_lower or "traffic" in cat_lower:
            severity = 7.0
            urgency = 6.5
        elif "waste" in cat_lower or "pollution" in cat_lower:
            severity = 6.5
            urgency = 6.0
        else:
            severity = 5.0
            urgency = 5.0

        # Escalate severity if public health hazard or accident risk is explicitly mentioned
        hazard_words = ["accident", "injury", "hospital", "contamination", "illness", "hazard", "skidding", "flooding"]
        found_hazards = [w for w in hazard_words if any(w in c.lower() for c in all_consequences)]
        if found_hazards:
            severity = min(10.0, severity + 1.5)
            urgency = min(10.0, urgency + 1.0)

        # 4. Community impact & Actionability
        community_impact = min(10.0, 4.0 + (distinct_source_count * 1.5))
        actionability = 7.5  # Citizen audit and official grievance filing are viable

        # 5. Composite priority score (0 - 100)
        composite = (
            (severity * 0.25) +
            (community_impact * 0.20) +
            (urgency * 0.15) +
            (recurrence_score * 0.15) +
            (evidence_score * 0.15) +
            (actionability * 0.10)
        ) * 10.0

        issue.severity_score = round(severity, 1)
        issue.urgency_score = round(urgency, 1)
        issue.recurrence_score = round(recurrence_score, 1)
        issue.evidence_strength_score = round(evidence_score, 1)
        issue.community_impact_score = round(community_impact, 1)
        issue.actionability_score = round(actionability, 1)
        issue.composite_priority_score = round(composite, 1)

        issue.score_reasons = {
            "severity_reasons": f"Base category rating for '{issue.category}' plus observed consequences: {', '.join(all_consequences[:2]) or 'None reported'}.",
            "evidence_reasons": f"Corroborated by {distinct_source_count} distinct publisher(s) with {len(all_evidence)} verified quote(s).",
            "recurrence_reasons": f"Pattern classified as {issue.recurrence_pattern} over span of {time_span_days} days across {len(observations)} observation(s).",
            "urgency_reasons": f"Assessed at {urgency}/10 due to imminent pedestrian/commuter disruption.",
            "community_impact_reasons": f"Impacts commuters and residents in {issue.normalized_location or 'reported area'}.",
            "actionability_reasons": "Constructive citizen photo audit and formal grievance escalation are feasible.",
        }

        # Update intelligence report fields
        issue.what_is_happening = issue.summary
        issue.where_is_it_happening = issue.normalized_location or "Reported Municipal Ward Corridor"
        issue.unverified_information = list(set(all_missing))[:5]
        issue.affected_stakeholders_summary = f"Pedestrians, vehicular commuters, and local residential colonies in {issue.normalized_location}."
        issue.recommended_practical_action = (
            f"Coordinate a daytime photo audit of defects in {issue.normalized_location} and log formal complaints "
            f"on the official municipal grievance portal."
        )

        self.db.commit()
        return issue
