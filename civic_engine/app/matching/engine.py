"""Hybrid matching and deduplication engine for civic issues."""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.location.resolver import haversine_distance_km
from app.schemas.common import IssueRelationshipType

logger = logging.getLogger(__name__)


def compute_text_similarity(text1: str, text2: str) -> float:
    """Calculate TF-IDF cosine similarity between two texts."""
    t1 = (text1 or "").strip()
    t2 = (text2 or "").strip()
    if not t1 or not t2:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([t1, t2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(max(0.0, min(1.0, sim)))
    except Exception as e:
        logger.warning(f"TF-IDF similarity calculation failed, falling back to Jaccard: {e}")
        words1 = set(t1.lower().split())
        words2 = set(t2.lower().split())
        if not words1 or not words2:
            return 0.0
        return float(len(words1 & words2) / len(words1 | words2))


class MatchEvaluationResult:
    """Outcome of comparing two civic issue observations or consolidated issues."""
    def __init__(
        self,
        relationship_type: IssueRelationshipType,
        similarity_score: float,
        match_reasons: List[str],
        is_merge_candidate: bool,
    ):
        self.relationship_type = relationship_type
        self.similarity_score = round(similarity_score, 3)
        self.match_reasons = match_reasons
        self.is_merge_candidate = is_merge_candidate


def evaluate_issue_pair(
    title1: str,
    desc1: str,
    cat1: str,
    loc1: Optional[str],
    lat1: Optional[float],
    lon1: Optional[float],
    date1: Optional[datetime],
    title2: str,
    desc2: str,
    cat2: str,
    loc2: Optional[str],
    lat2: Optional[float],
    lon2: Optional[float],
    date2: Optional[datetime],
) -> MatchEvaluationResult:
    """
    Hybrid multi-factor evaluation of two issues:
    1. Category compatibility
    2. Geographic distance & locality match
    3. Temporal separation
    4. Text description & title semantic similarity
    """
    reasons = []

    # 1. Category comparison
    same_category = (cat1.lower() == cat2.lower())
    if not same_category:
        reasons.append(f"Distinct civic categories: '{cat1}' vs '{cat2}'")

    # 2. Text similarity
    text1 = f"{title1} {desc1}"
    text2 = f"{title2} {desc2}"
    text_sim = compute_text_similarity(text1, text2)
    reasons.append(f"Text similarity score: {text_sim:.2f}")

    # 3. Geographic comparison
    geo_distance_km = None
    same_spot = False
    nearby = False
    same_locality_name = False

    if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
        geo_distance_km = haversine_distance_km(lat1, lon1, lat2, lon2)
        if geo_distance_km <= 0.6:
            same_spot = True
            reasons.append(f"Exact geographic match: {geo_distance_km:.2f} km distance")
        elif geo_distance_km <= 3.5:
            nearby = True
            reasons.append(f"Nearby spatial proximity: {geo_distance_km:.2f} km distance")
        else:
            reasons.append(f"Geographically distant: {geo_distance_km:.2f} km apart")
    elif loc1 and loc2:
        norm1 = loc1.lower().strip()
        norm2 = loc2.lower().strip()
        if norm1 == norm2 or norm1 in norm2 or norm2 in norm1:
            same_locality_name = True
            same_spot = True
            reasons.append(f"Matching named locality: '{loc1}'")

    # 4. Temporal comparison
    temporal_delta_days = None
    if date1 and date2:
        temporal_delta_days = abs((date1 - date2).days)
        reasons.append(f"Observation time gap: {temporal_delta_days} days")

    # 5. Relationship Classification Logic
    if not same_category:
        if text_sim > 0.4:
            return MatchEvaluationResult(
                relationship_type=IssueRelationshipType.UNRELATED_KEYWORD_MATCH,
                similarity_score=min(0.4, text_sim * 0.5),
                match_reasons=reasons + ["Overlapping vocabulary between fundamentally different civic categories."],
                is_merge_candidate=False,
            )
        return MatchEvaluationResult(
            relationship_type=IssueRelationshipType.UNRELATED_KEYWORD_MATCH,
            similarity_score=0.1,
            match_reasons=reasons + ["Different categories and unrelated incident context."],
            is_merge_candidate=False,
        )

    # If same category:
    if same_spot:
        # Same category + same location
        if temporal_delta_days is not None and temporal_delta_days > 14:
            # Recurring problem over extended time!
            score = 0.85 + (text_sim * 0.15)
            return MatchEvaluationResult(
                relationship_type=IssueRelationshipType.RECURRING_INCIDENT,
                similarity_score=score,
                match_reasons=reasons + ["Chronic / recurring municipal defect identified at the same facility."],
                is_merge_candidate=True,
            )
        else:
            # Within 14 days or no date gap -> duplicate report of same incident
            score = 0.80 + (text_sim * 0.20)
            return MatchEvaluationResult(
                relationship_type=IssueRelationshipType.DUPLICATE_REPORT,
                similarity_score=score,
                match_reasons=reasons + ["Multiple sources describing the same ongoing incident."],
                is_merge_candidate=True,
            )

    elif nearby:
        # Same category + nearby location
        score = 0.60 + (text_sim * 0.30)
        return MatchEvaluationResult(
            relationship_type=IssueRelationshipType.NEARBY_SIMILAR,
            similarity_score=score,
            match_reasons=reasons + ["Similar civic issue in neighboring ward or corridor."],
            is_merge_candidate=False,
        )

    else:
        # Same category, but distant or unspecified location
        score = 0.40 + (text_sim * 0.40)
        return MatchEvaluationResult(
            relationship_type=IssueRelationshipType.CROSS_AREA_SIMILAR,
            similarity_score=score,
            match_reasons=reasons + ["Similar civic problem type occurring in separate municipal zones."],
            is_merge_candidate=False,
        )
