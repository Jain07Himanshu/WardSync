"""Base abstract class defining the common interface for all AI Providers."""

import abc
import json
import logging
import time
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.core.exceptions import ConfigurationError, ProviderError, ValidationError
from app.core.security import frame_untrusted_content_for_prompt
from app.schemas.issue import ExtractedIssueSchema
from app.schemas.stakeholder import StakeholderRecommendationSchema
from app.schemas.opportunity import CivicActionPlanSchema

logger = logging.getLogger(__name__)


class BaseAIProvider(abc.ABC):
    """
    Common provider-independent interface for GenAI services.
    Enforces identical method signatures across OpenAI, Gemini, Anthropic, and Mock providers.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.effective_model
        self.timeout = settings.REQUEST_TIMEOUT_SECONDS
        self.max_retries = settings.MAX_RETRIES
        self.backoff_factor = settings.BACKOFF_FACTOR

    @property
    @abc.abstractmethod
    def provider_name(self) -> str:
        """Return the lowercase name of the AI provider."""
        pass

    @abc.abstractmethod
    def analyze_source(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Comprehensive preliminary analysis of untrusted source text.
        Extracts summary, detected civic themes, affected areas, and language.
        """
        pass

    @abc.abstractmethod
    def extract_civic_issues(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> List[ExtractedIssueSchema]:
        """
        Extract zero or more structured civic issues from source content.
        Validates output against ExtractedIssueSchema.
        """
        pass

    @abc.abstractmethod
    def classify_issue(self, issue_description: str) -> Dict[str, Any]:
        """
        Categorize an issue into standard civic taxonomy with subcategory and confidence.
        """
        pass

    @abc.abstractmethod
    def find_related_issues(self, target_issue: Dict[str, Any], candidate_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Perform semantic cross-evaluation of issues to identify relationships:
        DUPLICATE_REPORT, RECURRING_INCIDENT, NEARBY_SIMILAR, CROSS_AREA_SIMILAR, UNRELATED_KEYWORD_MATCH.
        """
        pass

    @abc.abstractmethod
    def identify_stakeholders(self, issue_data: Dict[str, Any], jurisdiction_info: Optional[Dict[str, Any]] = None) -> List[StakeholderRecommendationSchema]:
        """
        Identify responsible or relevant civic authorities, ward offices, and civil society groups.
        """
        pass

    @abc.abstractmethod
    def generate_civic_action(self, issue_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> List[CivicActionPlanSchema]:
        """
        Generate practical, safe citizen action and volunteer opportunities for an issue.
        """
        pass

    @abc.abstractmethod
    def evaluate_evidence(self, issue_data: Dict[str, Any], evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate the reliability, sufficiency, and corroboration of evidence for an issue.
        """
        pass

    # Aliases for camelCase naming matching instructions
    def analyzeSource(self, *args, **kwargs):
        return self.analyze_source(*args, **kwargs)

    def extractCivicIssues(self, *args, **kwargs):
        return self.extract_civic_issues(*args, **kwargs)

    def classifyIssue(self, *args, **kwargs):
        return self.classify_issue(*args, **kwargs)

    def findRelatedIssues(self, *args, **kwargs):
        return self.find_related_issues(*args, **kwargs)

    def identifyStakeholders(self, *args, **kwargs):
        return self.identify_stakeholders(*args, **kwargs)

    def generateCivicAction(self, *args, **kwargs):
        return self.generate_civic_action(*args, **kwargs)

    def evaluateEvidence(self, *args, **kwargs):
        return self.evaluate_evidence(*args, **kwargs)

    def execute_with_retry(self, operation_name: str, func, *args, **kwargs):
        """
        Execute an external AI call with exponential backoff and transparent error handling.
        """
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                last_error = exc
                wait_time = self.backoff_factor ** attempt
                logger.warning(
                    f"[{self.provider_name}] Attempt {attempt}/{self.max_retries} failed for {operation_name}: {exc}. "
                    f"Retrying in {wait_time:.1f}s..."
                )
                if attempt < self.max_retries:
                    time.sleep(wait_time)

        logger.error(f"[{self.provider_name}] All {self.max_retries} retries exhausted for {operation_name}: {last_error}")
        raise ProviderError(
            message=f"Provider {self.provider_name} failed on {operation_name}: {str(last_error)}",
            provider=self.provider_name,
            retryable=False
        )

    def clean_json_response(self, raw_text: str) -> str:
        """Strip markdown code block indicators from LLM responses."""
        text = raw_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
