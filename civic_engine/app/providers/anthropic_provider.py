"""Anthropic Claude API Provider using official anthropic SDK."""

import json
import logging
from typing import List, Dict, Any, Optional

try:
    from anthropic import Anthropic, APIError, AuthenticationError, RateLimitError
except ImportError:
    Anthropic = None
    APIError = None
    AuthenticationError = None
    RateLimitError = None

from app.core.config import settings
from app.core.exceptions import ConfigurationError, ProviderError, ValidationError
from app.core.security import frame_untrusted_content_for_prompt
from app.providers.base import BaseAIProvider
from app.schemas.common import CIVIC_CATEGORIES_LIST
from app.schemas.issue import ExtractedIssueSchema
from app.schemas.stakeholder import StakeholderRecommendationSchema
from app.schemas.opportunity import CivicActionPlanSchema

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude API implementation using official anthropic SDK."""

    def __init__(self, model_name: Optional[str] = None):
        super().__init__(model_name or "claude-3-5-sonnet-20241022")
        api_key = settings.ANTHROPIC_API_KEY
        if not api_key or not api_key.strip():
            raise ConfigurationError("ANTHROPIC_API_KEY is not configured in environment or .env file.")

        if Anthropic is None:
            raise ConfigurationError("anthropic package is not installed.")

        try:
            self.client = Anthropic(api_key=api_key, timeout=float(self.timeout))
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize Anthropic client: {e}")

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        def _invoke():
            try:
                # Instruct Claude to produce valid JSON only
                enhanced_system = f"{system_prompt}\nYou MUST output valid JSON only. Do not include introductory text or markdown outside of the JSON string."
                response = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=4096,
                    system=enhanced_system,
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=0.1,
                )
                text = response.content[0].text if response.content else "{}"
                return text
            except AuthenticationError as e:
                raise ProviderError(
                    message=f"Anthropic authentication failed: {e}",
                    provider="anthropic",
                    status_code=401,
                    retryable=False
                )
            except RateLimitError as e:
                raise ProviderError(
                    message=f"Anthropic rate limit exceeded: {e}",
                    provider="anthropic",
                    status_code=429,
                    retryable=True
                )
            except Exception as e:
                raise ProviderError(
                    message=f"Anthropic API call failed: {e}",
                    provider="anthropic",
                    status_code=502,
                    retryable=True
                )

        return self.execute_with_retry("anthropic_message", _invoke)

    def analyze_source(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        system = "Analyze the text and return JSON: summary, detected_language, relevance_score, contains_civic_complaint, potential_locations."
        user = frame_untrusted_content_for_prompt(source_text)
        raw = self._call_claude(system, user)
        try:
            data = json.loads(self.clean_json_response(raw))
            data["ai_provider"] = "anthropic"
            data["ai_model"] = self.model_name
            return data
        except Exception as e:
            raise ValidationError(f"Anthropic analysis parsing failed: {e}")

    def extract_civic_issues(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> List[ExtractedIssueSchema]:
        cats = ", ".join(f'"{c}"' for c in CIVIC_CATEGORIES_LIST)
        system = f"""
You are a civic issue extraction engine.
Allowed categories: [{cats}].
Return a JSON object with key "issues" containing array of objects:
- issue_title, problem_description, category, subcategory, location_mentioned, normalized_location,
  latitude, longitude, affected_population, first_reported_date, most_recent_observation_date,
  possible_causes, reported_consequences, evidence_excerpts, source_references, confidence_score,
  missing_information, verification_status, suggested_next_steps.
"""
        user = frame_untrusted_content_for_prompt(source_text)
        raw = self._call_claude(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return [ExtractedIssueSchema(**item) for item in parsed.get("issues", [])]
        except Exception as e:
            raise ValidationError(f"Anthropic issue extraction failed: {e}")

    def classify_issue(self, issue_description: str) -> Dict[str, Any]:
        cats = ", ".join(f'"{c}"' for c in CIVIC_CATEGORIES_LIST)
        system = f"Classify into [{cats}]. Return JSON: category, subcategory, confidence, reasoning."
        raw = self._call_claude(system, issue_description)
        try:
            return json.loads(self.clean_json_response(raw))
        except Exception as e:
            raise ValidationError(f"Anthropic classification failed: {e}")

    def find_related_issues(self, target_issue: Dict[str, Any], candidate_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not candidate_issues:
            return []
        system = "Classify relationships (DUPLICATE_REPORT, RECURRING_INCIDENT, NEARBY_SIMILAR, CROSS_AREA_SIMILAR, UNRELATED_KEYWORD_MATCH). Return JSON with key 'matches'."
        user = json.dumps({"target": target_issue, "candidates": candidate_issues})
        raw = self._call_claude(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return parsed.get("matches", [])
        except Exception as e:
            raise ValidationError(f"Anthropic find_related_issues failed: {e}")

    def identify_stakeholders(self, issue_data: Dict[str, Any], jurisdiction_info: Optional[Dict[str, Any]] = None) -> List[StakeholderRecommendationSchema]:
        system = "Identify responsible authorities and civic departments. NEVER invent fake numbers/emails. Return JSON key 'stakeholders'."
        user = json.dumps({"issue": issue_data, "jurisdiction": jurisdiction_info or {}})
        raw = self._call_claude(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return [StakeholderRecommendationSchema(**item) for item in parsed.get("stakeholders", [])]
        except Exception as e:
            raise ValidationError(f"Anthropic stakeholder recommendation failed: {e}")

    def generate_civic_action(self, issue_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> List[CivicActionPlanSchema]:
        system = "Generate safe citizen action plans. Return JSON with key 'plans'."
        user = json.dumps({"issue": issue_data, "context": context or {}})
        raw = self._call_claude(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return [CivicActionPlanSchema(**item) for item in parsed.get("plans", [])]
        except Exception as e:
            raise ValidationError(f"Anthropic action plan generation failed: {e}")

    def evaluate_evidence(self, issue_data: Dict[str, Any], evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        system = "Evaluate evidence sufficiency and gaps. Return JSON: evidence_count, evidence_strength_score, corroboration_level, has_firsthand_quotes, has_specific_dates, missing_key_factors, verification_recommendation."
        user = json.dumps({"issue": issue_data, "evidence": evidence_items})
        raw = self._call_claude(system, user)
        try:
            return json.loads(self.clean_json_response(raw))
        except Exception as e:
            raise ValidationError(f"Anthropic evidence evaluation failed: {e}")
