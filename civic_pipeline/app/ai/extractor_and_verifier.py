import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.schemas import (
    RawSignalInput,
    CivicVerificationResult,
    SourceType,
    CivicCategory,
    SeverityLevel,
)
from .gemini_client import get_gemini_client

logger = logging.getLogger("civic_pipeline.extractor")


class CivicExtractorAndVerifier:
    """
    Synthesizes multi-source civic problem signals into structured metadata,
    computes credibility scores via Google Gemini, and adjusts scores upon multi-source corroboration.
    """

    def __init__(self):
        self.ai_client = get_gemini_client()

    def process_raw_signals(self, signals: List[RawSignalInput]) -> CivicVerificationResult:
        """
        Synthesizes a collection of raw input signals (tweets, complaints, news articles, notices)
        and extracts verified civic issue metadata using Gemini 1.5 Flash.
        """
        aggregated_text = self._aggregate_signal_content(signals)
        logger.info("Extracting and verifying %d civic signals with Gemini", len(signals))
        
        result = self.ai_client.extract_and_verify(aggregated_text)

        # Apply multi-source corroboration bonuses to initial verification
        source_types = set(s.source_type for s in signals)
        if len(source_types) > 1:
            adjusted_score, added_reason = self.calculate_multi_source_bonus(
                base_score=result.authenticity_score,
                source_types=list(source_types),
                source_count=len(signals)
            )
            result.authenticity_score = adjusted_score
            result.authenticity_breakdown += f" | {added_reason}"

        return result

    def recalculate_authenticity_on_merge(
        self,
        current_score: int,
        existing_sources: List[Dict[str, Any]],
        new_source: RawSignalInput
    ) -> (int, str):
        """
        Recalculates authenticity score when an incoming post/article merges into an existing issue.
        Core rule: Authenticity increases significantly when independent news articles corroborate social media posts.
        """
        existing_types = set(s.get("source_type") for s in existing_sources)
        new_type = new_source.source_type.value

        score = current_score
        reasons = []

        # Corroboration Rule 1: Independent news corroborates social media or resident complaints
        if new_type == SourceType.NEWS.value and (
            SourceType.TWITTER.value in existing_types or SourceType.RESIDENT_COMPLAINT.value in existing_types
        ):
            boost = 18
            score += boost
            reasons.append(f"Independent journalistic news report corroborated earlier social/resident signals (+{boost} pts).")

        # Corroboration Rule 2: Social media/resident reports corroborate earlier reports
        elif new_type in (SourceType.TWITTER.value, SourceType.RESIDENT_COMPLAINT.value):
            if new_type in existing_types:
                boost = 6
                score += boost
                reasons.append(f"Additional independent resident signal reinforces existing reports (+{boost} pts).")
            else:
                boost = 10
                score += boost
                reasons.append(f"New signal type ({new_type}) cross-corroborates existing evidence (+{boost} pts).")

        # Corroboration Rule 3: Municipal notice corroboration
        elif new_type == SourceType.MUNICIPAL_NOTICE.value:
            boost = 20
            score += boost
            reasons.append(f"Official municipal administrative notice confirms issue presence (+{boost} pts).")

        # General multi-source volume reinforcement
        total_count = len(existing_sources) + 1
        if total_count >= 3 and score < 85:
            score += 5
            reasons.append(f"Consensus threshold reached with {total_count} aggregate sources (+5 pts).")

        # Cap score between 0 and 100
        score = max(0, min(100, score))
        explanation = " ".join(reasons) if reasons else "Source merged into cluster."

        return score, explanation

    def calculate_multi_source_bonus(
        self,
        base_score: int,
        source_types: List[SourceType],
        source_count: int
    ) -> (int, str):
        """Calculates initial cross-source boost if batch contains heterogeneous sources."""
        score = base_score
        types_set = set(source_types)
        reasons = []

        if SourceType.NEWS in types_set and (SourceType.TWITTER in types_set or SourceType.RESIDENT_COMPLAINT in types_set):
            boost = 15
            score += boost
            reasons.append("Multi-source batch contains cross-verification between journalistic news and citizen reports (+15 pts).")
        elif len(types_set) > 1:
            boost = 8
            score += boost
            reasons.append(f"Multi-source corroboration across {len(types_set)} distinct channels (+8 pts).")

        score = max(0, min(100, score))
        return score, " ".join(reasons)

    def _aggregate_signal_content(self, signals: List[RawSignalInput]) -> str:
        """Formats multiple signals into a structured text prompt for the model."""
        lines = []
        for i, s in enumerate(signals, 1):
            url_str = f" [URL: {s.source_url}]" if s.source_url else ""
            pub_str = f" [Time: {s.published_at.isoformat()}]" if s.published_at else ""
            lines.append(f"--- Signal {i} (Source: {s.source_type.value}{url_str}{pub_str}) ---\n{s.raw_content.strip()}")
        return "\n\n".join(lines)


_extractor_instance = None


def get_extractor_and_verifier() -> CivicExtractorAndVerifier:
    """Retrieve singleton instance of CivicExtractorAndVerifier."""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = CivicExtractorAndVerifier()
    return _extractor_instance
