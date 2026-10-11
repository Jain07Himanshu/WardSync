"""Google Gemini API Provider using official google-genai SDK."""

import json
import logging
from typing import List, Dict, Any, Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

from app.core.config import settings
from app.core.exceptions import ConfigurationError, ProviderError, ValidationError
from app.core.security import frame_untrusted_content_for_prompt
from app.providers.base import BaseAIProvider
from app.schemas.common import CIVIC_CATEGORIES_LIST
from app.schemas.issue import ExtractedIssueSchema
from app.schemas.stakeholder import StakeholderRecommendationSchema
from app.schemas.opportunity import CivicActionPlanSchema

logger = logging.getLogger(__name__)


class GeminiProvider(BaseAIProvider):
    """Google Gemini API implementation using official google-genai SDK."""

    def __init__(self, model_name: Optional[str] = None):
        super().__init__(model_name or "gemini-2.5-flash")
        api_key = settings.GEMINI_API_KEY
        if not api_key or not api_key.strip():
            raise ConfigurationError("GEMINI_API_KEY is not configured in environment or .env file.")

        if genai is None:
            raise ConfigurationError("google-genai package is not installed.")

        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize Gemini client: {e}")

    @property
    def provider_name(self) -> str:
        return "gemini"

    def _generate_json(self, system_instruction: str, contents: str) -> str:
        def _invoke():
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1,
                )
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config,
                )
                return response.text or "{}"
            except Exception as e:
                err_str = str(e).lower()
                is_auth = "api_key" in err_str or "unauthorized" in err_str or "permission" in err_str or "401" in err_str or "403" in err_str
                is_rate = "resource_exhausted" in err_str or "429" in err_str or "quota" in err_str
                raise ProviderError(
                    message=f"Gemini API invocation failed: {e}",
                    provider="gemini",
                    status_code=401 if is_auth else (429 if is_rate else 502),
                    retryable=is_rate
                )

        return self.execute_with_retry("gemini_generate", _invoke)

    def analyze_source(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        system = "You are a civic intelligence analyst. Return a JSON object with: summary, detected_language, relevance_score, contains_civic_complaint, potential_locations."
        user = frame_untrusted_content_for_prompt(source_text)
        raw = self._generate_json(system, user)
        try:
            data = json.loads(self.clean_json_response(raw))
            data["ai_provider"] = "gemini"
            data["ai_model"] = self.model_name
            return data
        except Exception as e:
            raise ValidationError(f"Gemini output parsing failed: {e}")

    def extract_civic_issues(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> List[ExtractedIssueSchema]:
        cats = ", ".join(f'"{c}"' for c in CIVIC_CATEGORIES_LIST)
        system = f"""
You are a civic issue extraction engine.
Allowed categories: [{cats}].
Extract all civic issues and return a JSON object with key "issues", containing an array of objects matching:
- issue_title (string)
- problem_description (string)
- category (string)
- subcategory (string or null)
- location_mentioned (string or null)
- normalized_location (string or null)
- latitude (float or null)
- longitude (float or null)
- affected_population (string)
- first_reported_date (string YYYY-MM-DD or null)
- most_recent_observation_date (string YYYY-MM-DD or null)
- possible_causes (list of strings)
- reported_consequences (list of strings)
- evidence_excerpts (list of strings quoting source)
- source_references (list of strings)
- confidence_score (float 0.0-1.0)
- missing_information (list of strings)
- verification_status ("UNVERIFIED", "COMMUNITY_REPORTED", "CORROBORATED")
- suggested_next_steps (list of strings)
"""
        user = frame_untrusted_content_for_prompt(source_text)
        raw = self._generate_json(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return [ExtractedIssueSchema(**item) for item in parsed.get("issues", [])]
        except Exception as e:
            raise ValidationError(f"Gemini issue extraction schema validation failed: {e}")

    def classify_issue(self, issue_description: str) -> Dict[str, Any]:
        cats = ", ".join(f'"{c}"' for c in CIVIC_CATEGORIES_LIST)
        system = f"Classify this issue into one of: [{cats}]. Return JSON: category, subcategory, confidence, reasoning."
        raw = self._generate_json(system, issue_description)
        try:
            return json.loads(self.clean_json_response(raw))
        except Exception as e:
            raise ValidationError(f"Gemini classification failed: {e}")

    def find_related_issues(self, target_issue: Dict[str, Any], candidate_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not candidate_issues:
            return []
        system = "Classify relationship types (DUPLICATE_REPORT, RECURRING_INCIDENT, NEARBY_SIMILAR, CROSS_AREA_SIMILAR, UNRELATED_KEYWORD_MATCH). Return JSON with key 'matches'."
        user = json.dumps({"target": target_issue, "candidates": candidate_issues})
        raw = self._generate_json(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return parsed.get("matches", [])
        except Exception as e:
            raise ValidationError(f"Gemini find_related_issues failed: {e}")

    def identify_stakeholders(self, issue_data: Dict[str, Any], jurisdiction_info: Optional[Dict[str, Any]] = None) -> List[StakeholderRecommendationSchema]:
        system = "Identify responsible authorities and civic departments. NEVER invent fake phone numbers or emails. Return JSON key 'stakeholders'."
        user = json.dumps({"issue": issue_data, "jurisdiction": jurisdiction_info or {}})
        raw = self._generate_json(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return [StakeholderRecommendationSchema(**item) for item in parsed.get("stakeholders", [])]
        except Exception as e:
            raise ValidationError(f"Gemini stakeholder recommendation failed: {e}")

    def generate_civic_action(self, issue_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> List[CivicActionPlanSchema]:
        system = "Generate safe citizen action plans. Return JSON with key 'plans'."
        user = json.dumps({"issue": issue_data, "context": context or {}})
        raw = self._generate_json(system, user)
        try:
            parsed = json.loads(self.clean_json_response(raw))
            return [CivicActionPlanSchema(**item) for item in parsed.get("plans", [])]
        except Exception as e:
            raise ValidationError(f"Gemini action plan generation failed: {e}")

    def evaluate_evidence(self, issue_data: Dict[str, Any], evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        system = "Evaluate evidence sufficiency, corroboration, and gaps. Return JSON: evidence_count, evidence_strength_score, corroboration_level, has_firsthand_quotes, has_specific_dates, missing_key_factors, verification_recommendation."
        user = json.dumps({"issue": issue_data, "evidence": evidence_items})
        raw = self._generate_json(system, user)
        try:
            return json.loads(self.clean_json_response(raw))
        except Exception as e:
            raise ValidationError(f"Gemini evidence evaluation failed: {e}")
