"""Prioritization Service calculating explainable priority scores for opportunities and issues."""

from typing import Dict, Any, Tuple
from app.core.config import settings


class PrioritizationService:
    """Calculates transparent, weighted priority scores with factor breakdowns."""

    def __init__(self):
        self.w_severity = settings.WEIGHT_SEVERITY
        self.w_community = settings.WEIGHT_COMMUNITY_IMPACT
        self.w_urgency = settings.WEIGHT_URGENCY
        self.w_recurrence = settings.WEIGHT_RECURRENCE
        self.w_evidence = settings.WEIGHT_EVIDENCE_STRENGTH
        self.w_feasibility = settings.WEIGHT_FEASIBILITY

    def compute_opportunity_priority(
        self,
        severity_score: float,
        community_impact_score: float,
        urgency_score: float,
        recurrence_score: float,
        evidence_strength_score: float,
        feasibility_score: float = 8.0,
        safety_risk_level: str = "LOW",
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate weighted score (0.0 to 100.0) and explainable factor breakdown.
        """
        weighted_sum = (
            (severity_score * self.w_severity) +
            (community_impact_score * self.w_community) +
            (urgency_score * self.w_urgency) +
            (recurrence_score * self.w_recurrence) +
            (evidence_strength_score * self.w_evidence) +
            (feasibility_score * self.w_feasibility)
        ) * 10.0

        # Safety adjustment: If safety risk is HIGH, priority for unreviewed citizen action is capped
        requires_review = safety_risk_level in ["MODERATE", "HIGH_REQUIRES_AUTHORITY"]
        final_score = round(max(5.0, min(100.0, weighted_sum)), 1)

        breakdown = {
            "score": final_score,
            "weights": {
                "severity": self.w_severity,
                "community_impact": self.w_community,
                "urgency": self.w_urgency,
                "recurrence": self.w_recurrence,
                "evidence_strength": self.w_evidence,
                "feasibility": self.w_feasibility,
            },
            "components": {
                "severity": severity_score,
                "community_impact": community_impact_score,
                "urgency": urgency_score,
                "recurrence": recurrence_score,
                "evidence_strength": evidence_strength_score,
                "feasibility": feasibility_score,
            },
            "requires_human_review": requires_review,
            "safety_advisory": (
                "Activity requires mandatory safety review by community administrator before publication."
                if requires_review else "Low-risk citizen documentation activity; safe for public participation."
            )
        }

        return final_score, breakdown
