"""Background worker and orchestration pipeline for asynchronous jobs."""

import datetime
import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.models import SourceProcessingJob, Source, ConsolidatedIssue
from app.extraction.service import ExtractionService
from app.matching.service import MatchingService
from app.intelligence.service import IntelligenceService
from app.stakeholders.service import StakeholderService
from app.opportunities.service import OpportunityService

logger = logging.getLogger(__name__)


def run_full_pipeline_for_source(source_id: str, job_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute complete end-to-end processing pipeline for a given source:
    1. Extraction of structured observations
    2. Consolidation & related-issue matching
    3. Multi-factor civic intelligence scoring
    4. Authority & stakeholder discovery
    5. Action & volunteer opportunity generation
    """
    db: Session = SessionLocal()
    job = None
    if job_id:
        job = db.query(SourceProcessingJob).filter(SourceProcessingJob.id == job_id).first()
        if job:
            job.status = "IN_PROGRESS"
            job.progress_percentage = 10
            db.commit()

    try:
        # Step 1: Issue Extraction (10% -> 40%)
        logger.info(f"[Job {job_id or 'sync'}] Step 1: Extracting issues for source {source_id}")
        extractor = ExtractionService(db)
        observations = extractor.process_source(source_id)
        if job:
            job.progress_percentage = 40
            job.processed_items = len(observations)
            db.commit()

        # Step 2: Consolidation & Matching (40% -> 60%)
        logger.info(f"[Job {job_id or 'sync'}] Step 2: Consolidating and matching observations")
        matcher = MatchingService(db)
        consolidated_issues = matcher.consolidate_unassigned_observations()
        if job:
            job.progress_percentage = 60
            db.commit()

        # Step 3: Intelligence, Stakeholders, Opportunities (60% -> 100%)
        intel_service = IntelligenceService(db)
        stakeholder_service = StakeholderService(db)
        opportunity_service = OpportunityService(db)

        opportunities_created = 0
        stakeholders_mapped = 0

        for issue in consolidated_issues:
            # Intelligence & scoring
            intel_service.analyze_consolidated_issue(issue.id)
            # Stakeholder discovery
            stk_res = stakeholder_service.discover_stakeholders_for_issue(issue.id)
            stakeholders_mapped += len(stk_res.stakeholders)
            # Opportunity generation
            opps = opportunity_service.generate_opportunities_for_issue(issue.id)
            opportunities_created += len(opps)
            # Cross-issue relationships
            matcher.find_related_issues(issue.id)

        summary = {
            "source_id": source_id,
            "observations_extracted": len(observations),
            "consolidated_issues_count": len(consolidated_issues),
            "stakeholders_mapped": stakeholders_mapped,
            "opportunities_created": opportunities_created,
        }

        if job:
            job.status = "COMPLETED"
            job.progress_percentage = 100
            job.completed_at = datetime.datetime.utcnow()
            job.result_summary = summary
            db.commit()

        logger.info(f"[Job {job_id or 'sync'}] Pipeline completed successfully: {summary}")
        return summary

    except Exception as e:
        logger.error(f"[Job {job_id or 'sync'}] Pipeline failed: {e}", exc_info=True)
        if job:
            job.status = "FAILED"
            job.error_details = str(e)
            job.completed_at = datetime.datetime.utcnow()
            db.commit()
        raise
    finally:
        db.close()
