import logging
from typing import List, Dict, Any, Optional, Tuple
from uuid import UUID, uuid4
from datetime import datetime, timezone

from ..config import get_settings
from ..database import get_repository
from .gemini_client import get_gemini_client
from .extractor_and_verifier import get_extractor_and_verifier
from ..models.schemas import (
    RawSignalInput,
    CivicVerificationResult,
    IssueStatus,
    SourceType,
)

logger = logging.getLogger("civic_pipeline.clustering")


class CivicClusteringEngine:
    """
    Computes vector embeddings via text-embedding-004, clusters incoming signals
    against existing civic issues via pgvector cosine similarity, merges evidence,
    and recalculates authenticity scores upon corroboration.
    """

    def __init__(self):
        self.settings = get_settings()
        self.ai_client = get_gemini_client()
        self.extractor = get_extractor_and_verifier()
        self.repo = get_repository()

    def process_and_cluster(
        self,
        signals: List[RawSignalInput]
    ) -> Tuple[Dict[str, Any], str, Optional[float], List[Dict[str, Any]]]:
        """
        Orchestrates ingestion, AI verification, embedding, and clustering.
        Returns:
            (issue_record, cluster_action ['merged_existing_cluster' | 'created_new_issue'], similarity_score, saved_sources)
        """
        if not signals:
            raise ValueError("No civic signals provided for ingestion.")

        # 1. First, save incoming signals into civic_sources with status='raw'
        saved_sources = []
        for s in signals:
            source_data = {
                "id": str(uuid4()),
                "source_type": s.source_type.value,
                "source_url": s.source_url,
                "raw_content": s.raw_content,
                "published_at": s.published_at.isoformat() if s.published_at else datetime.now(timezone.utc).isoformat(),
                "status": "raw"
            }
            saved = self.repo.insert_source(source_data)
            saved_sources.append(saved)

        # 2. Extract structured metadata & verification via Gemini 1.5 Flash
        verification: CivicVerificationResult = self.extractor.process_raw_signals(signals)

        # 3. Compute 768-dimensional embedding on the synthesized problem description & ward
        embedding_text = f"Category: {verification.category.value}. Ward: {verification.ward}. Title: {verification.title}. Description: {verification.summary}"
        embedding: List[float] = self.ai_client.generate_embedding(embedding_text)

        # 4. Search for existing similar issues in the same ward using cosine similarity >= threshold (0.82)
        similar_issues = self.repo.search_similar_issues(
            query_embedding=embedding,
            similarity_threshold=self.settings.SIMILARITY_THRESHOLD,
            match_count=self.settings.MATCH_LIMIT,
            filter_ward=verification.ward
        )

        # If no ward-specific match found, search across nearby clusters with strict threshold
        if not similar_issues:
            similar_issues = self.repo.search_similar_issues(
                query_embedding=embedding,
                similarity_threshold=self.settings.SIMILARITY_THRESHOLD,
                match_count=1,
                filter_ward=None
            )

        # 5. Check if we match an existing cluster (similarity >= threshold)
        if similar_issues:
            best_match = similar_issues[0]
            sim_score = best_match.get("similarity", 0.85)
            logger.info("Found existing matching cluster %s with similarity %.4f", best_match["id"], sim_score)
            
            # Merge evidence into existing issue
            issue_record = self._merge_into_existing_issue(
                existing_issue=best_match,
                new_signals=signals,
                saved_sources=saved_sources,
                new_verification=verification
            )
            return issue_record, "merged_existing_cluster", sim_score, saved_sources

        else:
            # 6. No cluster match (similarity < 0.82) -> Create new civic issue
            logger.info("No matching cluster found (sim < %.2f). Creating new civic issue.", self.settings.SIMILARITY_THRESHOLD)
            issue_record = self._create_new_issue(
                verification=verification,
                embedding=embedding,
                source_count=len(signals),
                saved_sources=saved_sources
            )
            return issue_record, "created_new_issue", None, saved_sources

    def _merge_into_existing_issue(
        self,
        existing_issue: Dict[str, Any],
        new_signals: List[RawSignalInput],
        saved_sources: List[Dict[str, Any]],
        new_verification: CivicVerificationResult
    ) -> Dict[str, Any]:
        """
        Merges new signals into an existing cluster:
        - Associates source IDs with existing issue ID
        - Increments source_count
        - Recalculates authenticity_score using corroboration rules
        - Updates verification_reasoning and status if threshold met
        """
        issue_id = str(existing_issue["id"])
        
        # Link sources to issue and set status='clustered'
        for s in saved_sources:
            self.repo.update_source(s["id"], {"issue_id": issue_id, "status": "clustered"})

        # Fetch existing sources for corroboration check
        current_sources = self.repo.get_sources_by_issue(issue_id)
        current_score = existing_issue.get("authenticity_score", 50)

        # Incrementally recalculate score for each new signal
        accumulated_score = current_score
        corroboration_notes = []
        for new_sig in new_signals:
            accumulated_score, note = self.extractor.recalculate_authenticity_on_merge(
                current_score=accumulated_score,
                existing_sources=current_sources,
                new_source=new_sig
            )
            corroboration_notes.append(note)

        # Update source count
        new_source_count = existing_issue.get("source_count", 1) + len(new_signals)

        # Determine status transition
        current_status = existing_issue.get("status", IssueStatus.FLAGGED_UNVERIFIED.value)
        new_status = current_status
        if accumulated_score >= self.settings.VERIFICATION_THRESHOLD:
            if current_status == IssueStatus.FLAGGED_UNVERIFIED.value:
                new_status = IssueStatus.VERIFIED_PENDING_NGO.value
        else:
            if current_status not in (IssueStatus.EVENT_ACTIVE.value, IssueStatus.RESOLVED.value):
                new_status = IssueStatus.FLAGGED_UNVERIFIED.value

        # Update reasoning
        prev_reasoning = existing_issue.get("verification_reasoning") or ""
        merged_reasoning = f"{prev_reasoning} | [Corroboration Update: {' '.join(corroboration_notes)}]".strip(" | ")

        updates = {
            "source_count": new_source_count,
            "authenticity_score": accumulated_score,
            "verification_reasoning": merged_reasoning,
            "status": new_status,
        }

        updated_issue = self.repo.update_issue(issue_id, updates)
        return updated_issue or {**existing_issue, **updates}

    def _create_new_issue(
        self,
        verification: CivicVerificationResult,
        embedding: List[float],
        source_count: int,
        saved_sources: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Creates a new record in civic_issues table.
        """
        issue_id = str(uuid4())
        initial_status = (
            IssueStatus.VERIFIED_PENDING_NGO.value
            if verification.authenticity_score >= self.settings.VERIFICATION_THRESHOLD
            else IssueStatus.FLAGGED_UNVERIFIED.value
        )

        issue_data = {
            "id": issue_id,
            "title": verification.title,
            "summary": verification.summary,
            "category": verification.category.value,
            "ward": verification.ward,
            "latitude": verification.coordinates.latitude,
            "longitude": verification.coordinates.longitude,
            "severity": verification.severity.value,
            "authenticity_score": verification.authenticity_score,
            "verification_reasoning": verification.authenticity_breakdown,
            "responsible_authority": verification.responsible_authority,
            "source_count": source_count,
            "embedding": embedding,
            "status": initial_status,
            # store the generated blueprint in metadata/reasoning for dispatch
            "action_blueprint": verification.suggested_action_blueprint.model_dump(),
        }

        created_issue = self.repo.insert_issue(issue_data)

        # Link sources to new issue
        for s in saved_sources:
            self.repo.update_source(s["id"], {"issue_id": issue_id, "status": "processed"})

        return created_issue


_clustering_engine_instance = None


def get_clustering_engine() -> CivicClusteringEngine:
    """Retrieve singleton instance of CivicClusteringEngine."""
    global _clustering_engine_instance
    if _clustering_engine_instance is None:
        _clustering_engine_instance = CivicClusteringEngine()
    return _clustering_engine_instance
