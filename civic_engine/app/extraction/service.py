"""Civic Issue Extraction Service for processing raw sources into structured observations."""

import datetime
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import Source, ExtractedIssueObservation, AuditEvent
from app.providers.factory import get_ai_provider
from app.location.resolver import resolve_location
from app.schemas.issue import ExtractedIssueSchema

logger = logging.getLogger(__name__)


class ExtractionService:
    """Coordinates AI provider issue extraction, location normalization, and observation storage."""

    def __init__(self, db: Session, ai_provider_override: Optional[str] = None):
        self.db = db
        self.provider = get_ai_provider(provider_name=ai_provider_override)

    def process_source(self, source_id: str) -> List[ExtractedIssueObservation]:
        """
        Process a source record through AI extraction.
        Extracts structured observations, validates schemas, resolves locations,
        and saves observations.
        """
        source = self.db.query(Source).filter(Source.id == source_id).first()
        if not source:
            raise ValueError(f"Source with id {source_id} not found.")

        source.processing_status = "PROCESSING"
        self.db.commit()

        try:
            metadata = {
                "source_id": source.id,
                "title": source.original_title,
                "publisher": source.publisher,
                "source_type": source.source_type,
            }

            raw_extracted: List[ExtractedIssueSchema] = self.provider.extract_civic_issues(
                source_text=source.extracted_text,
                metadata=metadata
            )

            created_observations: List[ExtractedIssueObservation] = []

            for item in raw_extracted:
                # Enhance location resolution
                loc_info = resolve_location(item.location_mentioned or item.normalized_location)
                final_norm_loc = item.normalized_location or loc_info["normalized_location"]
                final_lat = item.latitude if item.latitude is not None else loc_info["latitude"]
                final_lon = item.longitude if item.longitude is not None else loc_info["longitude"]

                # Parse dates safely
                first_date = None
                if item.first_reported_date:
                    try:
                        first_date = datetime.datetime.fromisoformat(item.first_reported_date.replace("Z", ""))
                    except Exception:
                        pass

                obs_date = None
                if item.most_recent_observation_date:
                    try:
                        obs_date = datetime.datetime.fromisoformat(item.most_recent_observation_date.replace("Z", ""))
                    except Exception:
                        pass

                observation = ExtractedIssueObservation(
                    source_id=source.id,
                    issue_title=item.issue_title,
                    problem_description=item.problem_description,
                    category=item.category,
                    subcategory=item.subcategory,
                    location_mentioned=item.location_mentioned,
                    normalized_location=final_norm_loc,
                    latitude=final_lat,
                    longitude=final_lon,
                    affected_population=item.affected_population,
                    first_reported_date=first_date,
                    most_recent_observation_date=obs_date,
                    possible_causes=item.possible_causes,
                    reported_consequences=item.reported_consequences,
                    evidence_excerpts=item.evidence_excerpts,
                    missing_information=item.missing_information,
                    verification_status=item.verification_status,
                    confidence_score=item.confidence_score,
                    language=source.language,
                    suggested_next_steps=item.suggested_next_steps,
                    ai_provider=self.provider.provider_name,
                    ai_model=self.provider.model_name,
                    raw_ai_response=item.model_dump(),
                )
                self.db.add(observation)
                created_observations.append(observation)

            source.processing_status = "COMPLETED"
            self.db.flush()

            # Record audit
            audit = AuditEvent(
                event_type="ISSUES_EXTRACTED",
                entity_type="Source",
                entity_id=source.id,
                ai_provider=self.provider.provider_name,
                ai_model=self.provider.model_name,
                details={
                    "extracted_count": len(created_observations),
                    "categories": [o.category for o in created_observations],
                }
            )
            self.db.add(audit)
            self.db.commit()

            return created_observations

        except Exception as e:
            self.db.rollback()
            source.processing_status = "FAILED"
            source.error_message = str(e)
            self.db.commit()
            logger.error(f"Issue extraction failed for source {source_id}: {e}")
            raise
