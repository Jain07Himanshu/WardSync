"""Service layer for consolidating observations and discovering related issues."""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.models import (
    ExtractedIssueObservation,
    ConsolidatedIssue,
    IssueRelationship,
    Source,
    AuditEvent,
)
from app.matching.engine import evaluate_issue_pair, MatchEvaluationResult
from app.schemas.common import IssueRelationshipType

logger = logging.getLogger(__name__)


class MatchingService:
    """Manages deduplication, consolidation, and cross-issue relationship analysis."""

    def __init__(self, db: Session):
        self.db = db

    def consolidate_unassigned_observations(self) -> List[ConsolidatedIssue]:
        """
        Iterate through observations that have not yet been assigned to a consolidated issue.
        Either merges them into an existing ConsolidatedIssue or creates a new one.
        """
        unassigned = self.db.query(ExtractedIssueObservation).filter(
            ExtractedIssueObservation.consolidated_issue_id.is_(None)
        ).all()

        consolidated_results: List[ConsolidatedIssue] = []

        for obs in unassigned:
            existing_issues = self.db.query(ConsolidatedIssue).all()
            best_match: Optional[Tuple[ConsolidatedIssue, MatchEvaluationResult]] = None
            highest_score = 0.0

            for issue in existing_issues:
                eval_res = evaluate_issue_pair(
                    title1=obs.issue_title,
                    desc1=obs.problem_description,
                    cat1=obs.category,
                    loc1=obs.normalized_location,
                    lat1=obs.latitude,
                    lon1=obs.longitude,
                    date1=obs.most_recent_observation_date or obs.created_at,
                    title2=issue.title,
                    desc2=issue.summary,
                    cat2=issue.category,
                    loc2=issue.normalized_location,
                    lat2=issue.latitude,
                    lon2=issue.longitude,
                    date2=issue.last_seen_date or issue.created_at,
                )

                if eval_res.is_merge_candidate and eval_res.similarity_score > highest_score and eval_res.similarity_score >= 0.70:
                    highest_score = eval_res.similarity_score
                    best_match = (issue, eval_res)

            if best_match:
                # Merge observation into existing consolidated issue
                target_issue, eval_res = best_match
                obs.consolidated_issue_id = target_issue.id
                target_issue.observation_count += 1

                # Update dates
                obs_date = obs.most_recent_observation_date or obs.created_at
                if obs_date:
                    if target_issue.first_seen_date is None or obs_date < target_issue.first_seen_date:
                        target_issue.first_seen_date = obs_date
                    if target_issue.last_seen_date is None or obs_date > target_issue.last_seen_date:
                        target_issue.last_seen_date = obs_date

                # Recurrence tracking
                if eval_res.relationship_type == IssueRelationshipType.RECURRING_INCIDENT:
                    target_issue.is_recurring = True
                    target_issue.recurrence_pattern = "RECURRING_CHRONIC"
                    target_issue.recurrence_score = min(10.0, target_issue.recurrence_score + 2.5)

                # Distinct publishers count
                publishers = self.db.query(Source.publisher).join(
                    ExtractedIssueObservation, ExtractedIssueObservation.source_id == Source.id
                ).filter(ExtractedIssueObservation.consolidated_issue_id == target_issue.id).distinct().all()
                target_issue.distinct_publishers_count = len(publishers)

                # Update verification level based on distinct publisher corroboration
                if target_issue.distinct_publishers_count > 1:
                    target_issue.verification_level = "CROSS_SOURCE_CORROBORATED"

                # Audit
                audit = AuditEvent(
                    event_type="ISSUES_MERGED",
                    entity_type="ConsolidatedIssue",
                    entity_id=target_issue.id,
                    details={
                        "observation_id": obs.id,
                        "relationship_type": eval_res.relationship_type.value,
                        "similarity_score": eval_res.similarity_score,
                        "match_reasons": eval_res.match_reasons,
                    }
                )
                self.db.add(audit)
                consolidated_results.append(target_issue)

            else:
                # Create a new ConsolidatedIssue record
                new_issue = ConsolidatedIssue(
                    title=obs.issue_title,
                    summary=obs.problem_description,
                    category=obs.category,
                    subcategory=obs.subcategory,
                    normalized_location=obs.normalized_location,
                    latitude=obs.latitude,
                    longitude=obs.longitude,
                    observation_count=1,
                    distinct_publishers_count=1,
                    first_seen_date=obs.first_reported_date or obs.created_at,
                    last_seen_date=obs.most_recent_observation_date or obs.created_at,
                    is_recurring=False,
                    recurrence_pattern="SINGLE_INCIDENT",
                    trend_direction="NEW",
                    verification_level="SINGLE_UNVERIFIED",
                    severity_score=6.0,
                    urgency_score=5.0,
                    recurrence_score=1.0,
                    evidence_strength_score=5.0,
                    community_impact_score=5.0,
                    actionability_score=6.0,
                    composite_priority_score=55.0,
                    what_is_happening=obs.problem_description,
                    where_is_it_happening=obs.normalized_location or obs.location_mentioned,
                    unverified_information=obs.missing_information or [],
                    recommended_practical_action="Conduct initial field documentation and report to ward authorities.",
                )
                self.db.add(new_issue)
                self.db.flush()

                obs.consolidated_issue_id = new_issue.id
                consolidated_results.append(new_issue)

        self.db.commit()
        return consolidated_results

    def find_related_issues(self, issue_id: str) -> List[Dict[str, Any]]:
        """Find and record cross-issue relationships for a specific consolidated issue."""
        target = self.db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
        if not target:
            raise ValueError(f"ConsolidatedIssue {issue_id} not found.")

        candidates = self.db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id != issue_id).all()
        matches = []

        for cand in candidates:
            eval_res = evaluate_issue_pair(
                title1=target.title,
                desc1=target.summary,
                cat1=target.category,
                loc1=target.normalized_location,
                lat1=target.latitude,
                lon1=target.longitude,
                date1=target.last_seen_date,
                title2=cand.title,
                desc2=cand.summary,
                cat2=cand.category,
                loc2=cand.normalized_location,
                lat2=cand.latitude,
                lon2=cand.longitude,
                date2=cand.last_seen_date,
            )

            # Persist or update relationship in database
            existing_rel = self.db.query(IssueRelationship).filter(
                IssueRelationship.source_issue_id == target.id,
                IssueRelationship.target_issue_id == cand.id,
            ).first()

            if not existing_rel:
                rel = IssueRelationship(
                    source_issue_id=target.id,
                    target_issue_id=cand.id,
                    relationship_type=eval_res.relationship_type.value,
                    similarity_score=eval_res.similarity_score,
                    match_reasons=eval_res.match_reasons,
                )
                self.db.add(rel)

            matches.append({
                "target_issue_id": cand.id,
                "target_title": cand.title,
                "relationship_type": eval_res.relationship_type,
                "similarity_score": eval_res.similarity_score,
                "match_reasons": eval_res.match_reasons,
            })

        self.db.commit()
        # Sort by similarity score descending
        matches.sort(key=lambda x: x["similarity_score"], reverse=True)
        return matches
