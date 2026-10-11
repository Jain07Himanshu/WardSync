from app.matching.engine import (
    compute_text_similarity,
    evaluate_issue_pair,
    MatchEvaluationResult,
)
from app.matching.service import MatchingService

__all__ = [
    "compute_text_similarity",
    "evaluate_issue_pair",
    "MatchEvaluationResult",
    "MatchingService",
]
