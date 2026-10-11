"""Stakeholder discovery service coordinating verified directories and AI recommendations."""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.models import (
    ConsolidatedIssue,
    Stakeholder,
    IssueStakeholderMapping,
    AuditEvent,
)
from app.stakeholders.registry import VERIFIED_STAKEHOLDER_DIRECTORY
from app.providers.factory import get_ai_provider
from app.schemas.stakeholder import (
    IssueStakeholderResponse,
    StakeholderDiscoveryResult,
)

logger = logging.getLogger(__name__)


class StakeholderService:
    """Manages statutory authority directories and issue-stakeholder discovery."""

    def __init__(self, db: Session, ai_provider_override: Optional[str] = None):
        self.db = db
        self.provider = get_ai_provider(provider_name=ai_provider_override)
        self._ensure_registry_seeded()

    def _ensure_registry_seeded(self) -> None:
        """Seed verified authorities and NGOs if the stakeholder table is empty."""
        count = self.db.query(Stakeholder).count()
        if count == 0:
            logger.info("Seeding verified stakeholder directory into database.")
            for item in VERIFIED_STAKEHOLDER_DIRECTORY:
                stk = Stakeholder(
                    name=item["name"],
                    department=item["department"],
                    jurisdiction_level=item["jurisdiction_level"],
                    jurisdiction_area=item["jurisdiction_area"],
                    categories_handled=item["categories_handled"],
                    official_website=item["official_website"],
                    public_portal_url=item["public_portal_url"],
                    public_helpline=item["public_helpline"],
                    public_email=item["public_email"],
                    grievance_redressal_mechanism=item["grievance_redressal_mechanism"],
                    is_verified_in_registry=True,
                )
                self.db.add(stk)
            self.db.commit()

    def discover_stakeholders_for_issue(self, issue_id: str) -> StakeholderDiscoveryResult:
        """
        Identify verified and candidate authorities for an issue without fabricating contacts.
        """
        issue = self.db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
        if not issue:
            raise ValueError(f"ConsolidatedIssue {issue_id} not found.")

        # 1. Match from verified local registry based on category and jurisdiction area
        db_stakeholders = self.db.query(Stakeholder).all()
        matched_verified: List[Tuple[Stakeholder, str]] = []

        loc_lower = (issue.normalized_location or "").lower()
        for stk in db_stakeholders:
            category_match = issue.category in (stk.categories_handled or [])
            area_match = stk.jurisdiction_area.lower() in loc_lower or ("mumbai" in loc_lower and "mumbai" in stk.jurisdiction_area.lower())

            if category_match and (area_match or stk.jurisdiction_level in ["STATE", "NGO_COMMUNITY"]):
                relevance = f"Statutory authority for {issue.category} in {stk.jurisdiction_area}."
                matched_verified.append((stk, relevance))

        # 2. Call AI provider for contextual recommendations
        issue_payload = {
            "id": issue.id,
            "title": issue.title,
            "category": issue.category,
            "subcategory": issue.subcategory,
            "normalized_location": issue.normalized_location,
            "ward_zone": issue.ward_zone,
        }
        jurisdiction_info = {
            "jurisdiction_name": issue.jurisdiction_name,
            "ward_zone": issue.ward_zone,
        }

        ai_recommendations = self.provider.identify_stakeholders(issue_payload, jurisdiction_info)

        # 3. Persist and reconcile mappings
        created_responses: List[IssueStakeholderResponse] = []

        # Add verified matches
        for stk, reason in matched_verified:
            existing = self.db.query(IssueStakeholderMapping).filter(
                IssueStakeholderMapping.issue_id == issue.id,
                IssueStakeholderMapping.stakeholder_id == stk.id,
            ).first()

            if not existing:
                mapping = IssueStakeholderMapping(
                    issue_id=issue.id,
                    stakeholder_id=stk.id,
                    candidate_name=stk.name,
                    relevance_reason=reason,
                    jurisdiction_coverage=stk.jurisdiction_area,
                    verification_status="VERIFIED_REGISTRY",
                    confidence_level=0.95,
                    source_reference="Verified Municipal Jurisdiction Registry",
                )
                self.db.add(mapping)
                self.db.flush()
                existing = mapping

            created_responses.append(
                IssueStakeholderResponse(
                    id=existing.id,
                    issue_id=issue.id,
                    stakeholder_id=stk.id,
                    candidate_name=stk.name,
                    department=stk.department,
                    relevance_reason=existing.relevance_reason,
                    jurisdiction_coverage=stk.jurisdiction_area,
                    official_website=stk.official_website,
                    public_portal_url=stk.public_portal_url,
                    public_helpline=stk.public_helpline,
                    public_email=stk.public_email,
                    grievance_redressal_mechanism=stk.grievance_redressal_mechanism,
                    verification_status="VERIFIED_REGISTRY",
                    confidence_level=0.95,
                    source_reference="Verified Municipal Directory",
                    created_at=existing.created_at,
                )
            )

        # Add AI recommendations that are not already present
        for rec in ai_recommendations:
            # Check if this name matches an existing mapped name
            already_mapped = any(rec.organization_name.lower() in resp.candidate_name.lower() for resp in created_responses)
            if not already_mapped:
                mapping = IssueStakeholderMapping(
                    issue_id=issue.id,
                    stakeholder_id=None,
                    candidate_name=rec.organization_name,
                    relevance_reason=rec.relevance_reason,
                    jurisdiction_coverage=rec.jurisdiction_area,
                    verification_status="CANDIDATE_UNVERIFIED",
                    confidence_level=rec.confidence_level,
                    source_reference=rec.source_reference or f"{self.provider.provider_name} Suggestion",
                )
                self.db.add(mapping)
                self.db.flush()

                created_responses.append(
                    IssueStakeholderResponse(
                        id=mapping.id,
                        issue_id=issue.id,
                        stakeholder_id=None,
                        candidate_name=rec.organization_name,
                        department=rec.department,
                        relevance_reason=rec.relevance_reason,
                        jurisdiction_coverage=rec.jurisdiction_area,
                        official_website=None,
                        public_portal_url=rec.public_portal_or_contact_hint,
                        public_helpline=None,  # Never invent phone numbers
                        public_email=None,     # Never invent emails
                        grievance_redressal_mechanism=rec.public_portal_or_contact_hint,
                        verification_status="CANDIDATE_UNVERIFIED",
                        confidence_level=rec.confidence_level,
                        source_reference=mapping.source_reference,
                        created_at=mapping.created_at,
                    )
                )

        self.db.commit()

        return StakeholderDiscoveryResult(
            issue_id=issue.id,
            issue_title=issue.title,
            stakeholders=created_responses,
            jurisdiction_matched=issue.jurisdiction_name or "Municipal Administration",
            verification_notice="Contacts marked VERIFIED_REGISTRY originate from verified civic directories. Candidate stakeholders are unverified suggestions.",
        )
