"""Civic Action and Volunteer Opportunity Generator with safety guardrails."""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.models import (
    ConsolidatedIssue,
    CivicOpportunity,
    OpportunityReview,
    AuditEvent,
)
from app.providers.factory import get_ai_provider
from app.prioritization.service import PrioritizationService
from app.schemas.opportunity import (
    CivicActionPlanSchema,
    OpportunityReviewRequest,
)

logger = logging.getLogger(__name__)


class OpportunityService:
    """Generates structured, safe citizen action opportunities with prioritization."""

    def __init__(self, db: Session, ai_provider_override: Optional[str] = None):
        self.db = db
        self.provider = get_ai_provider(provider_name=ai_provider_override)
        self.prioritizer = PrioritizationService()

    def generate_opportunities_for_issue(self, issue_id: str) -> List[CivicOpportunity]:
        """
        Generate practical volunteer opportunities for a consolidated issue.
        Applies safety checks, computes priority scores, and persists to database.
        """
        issue = self.db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
        if not issue:
            raise ValueError(f"ConsolidatedIssue {issue_id} not found.")

        issue_payload = {
            "id": issue.id,
            "title": issue.title,
            "summary": issue.summary,
            "category": issue.category,
            "subcategory": issue.subcategory,
            "normalized_location": issue.normalized_location,
            "severity_score": issue.severity_score,
            "urgency_score": issue.urgency_score,
        }

        # Request action plans from AI provider
        generated_plans: List[CivicActionPlanSchema] = self.provider.generate_civic_action(
            issue_data=issue_payload,
            context={"jurisdiction": issue.jurisdiction_name, "ward": issue.ward_zone}
        )

        created_opportunities: List[CivicOpportunity] = []

        for plan in generated_plans:
            # Enforce safety guardrail:
            # If hazardous keywords detected in steps, escalate safety risk level
            plan_text = " ".join(plan.step_by_step_plan + plan.safety_considerations).lower()
            risk_level = plan.safety_risk_level
            if any(w in plan_text for w in ["electric", "wire", "chemical", "sewage", "high voltage", "confront"]):
                risk_level = "HIGH_REQUIRES_AUTHORITY"

            # Calculate transparent priority score
            p_score, p_breakdown = self.prioritizer.compute_opportunity_priority(
                severity_score=issue.severity_score,
                community_impact_score=issue.community_impact_score,
                urgency_score=issue.urgency_score,
                recurrence_score=issue.recurrence_score,
                evidence_strength_score=issue.evidence_strength_score,
                feasibility_score=8.5 if not plan.is_official_authorization_required else 6.0,
                safety_risk_level=risk_level,
            )

            # High risk or auth-required actions must remain pending review
            review_status = "PENDING_REVIEW"

            opp = CivicOpportunity(
                issue_id=issue.id,
                title=plan.title,
                problem_summary=plan.problem_summary,
                why_needed=plan.why_needed,
                activity_type=plan.activity_type.value,
                step_by_step_plan=plan.step_by_step_plan,
                intended_beneficiaries=plan.intended_beneficiaries,
                suggested_roles=plan.suggested_roles,
                required_materials=plan.required_materials,
                estimated_effort_hours=plan.estimated_effort_hours,
                suggested_participant_count=plan.suggested_participant_count,
                potential_collaborators=plan.potential_collaborators,
                escalation_channel=plan.escalation_channel,
                expected_outcomes=plan.expected_outcomes,
                success_metrics=plan.success_metrics,
                safety_considerations=plan.safety_considerations,
                prerequisites_and_permissions=plan.prerequisites_and_permissions,
                is_official_authorization_required=plan.is_official_authorization_required,
                safety_risk_level=risk_level,
                ai_confidence=plan.ai_confidence,
                review_status=review_status,
                priority_score=p_score,
                priority_breakdown=p_breakdown,
            )
            self.db.add(opp)
            created_opportunities.append(opp)

        self.db.commit()

        # Audit event
        audit = AuditEvent(
            event_type="OPPORTUNITY_GENERATED",
            entity_type="ConsolidatedIssue",
            entity_id=issue.id,
            details={
                "opportunities_count": len(created_opportunities),
                "titles": [o.title for o in created_opportunities],
            }
        )
        self.db.add(audit)
        self.db.commit()

        return created_opportunities

    def review_opportunity(self, opportunity_id: str, review_in: OpportunityReviewRequest) -> OpportunityReview:
        """
        Record a human review decision (APPROVED, REJECTED, MODIFIED) on a generated opportunity.
        """
        opp = self.db.query(CivicOpportunity).filter(CivicOpportunity.id == opportunity_id).first()
        if not opp:
            raise ValueError(f"CivicOpportunity {opportunity_id} not found.")

        opp.review_status = review_in.status.value
        opp.review_notes = review_in.feedback_comments

        if review_in.modifications:
            for k, v in review_in.modifications.items():
                if hasattr(opp, k):
                    setattr(opp, k, v)

        review_audit = OpportunityReview(
            opportunity_id=opp.id,
            reviewer_name=review_in.reviewer_name,
            status=review_in.status.value,
            feedback_comments=review_in.feedback_comments,
            modifications=review_in.modifications or {},
        )
        self.db.add(review_audit)
        self.db.commit()

        return review_audit
