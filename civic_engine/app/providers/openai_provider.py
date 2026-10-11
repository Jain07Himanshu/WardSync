"""OpenAI API Provider implementation using official openai Python SDK."""

import json
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI, APIError, AuthenticationError, RateLimitError, APIConnectionError

from app.core.config import settings
from app.core.exceptions import ConfigurationError, ProviderError, ValidationError
from app.core.security import frame_untrusted_content_for_prompt
from app.providers.base import BaseAIProvider
from app.schemas.common import CIVIC_CATEGORIES_LIST, IssueRelationshipType
from app.schemas.issue import ExtractedIssueSchema
from app.schemas.stakeholder import StakeholderRecommendationSchema
from app.schemas.opportunity import CivicActionPlanSchema

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI implementation using official OpenAI SDK with structured JSON parsing."""

    def __init__(self, model_name: Optional[str] = None):
        super().__init__(model_name)
        api_key = settings.OPENAI_API_KEY
        if not api_key or not api_key.strip():
            raise ConfigurationError("OPENAI_API_KEY is not configured in environment or .env file.")

        try:
            self.client = OpenAI(
                api_key=api_key,
                timeout=float(self.timeout),
                max_retries=0  # We manage retries via execute_with_retry for transparent observability
            )
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize OpenAI client: {e}")

    @property
    def provider_name(self) -> str:
        return "openai"

    def _call_chat_completion(self, system_prompt: str, user_prompt: str) -> str:
        def _invoke():
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                )
                return response.choices[0].message.content or "{}"
            except AuthenticationError as e:
                raise ProviderError(
                    message=f"OpenAI authentication failed: Invalid API key. Error: {e}",
                    provider="openai",
                    status_code=401,
                    retryable=False
                )
            except RateLimitError as e:
                raise ProviderError(
                    message=f"OpenAI rate limit exceeded: {e}",
                    provider="openai",
                    status_code=429,
                    retryable=True
                )
            except (APIConnectionError, APIError) as e:
                raise ProviderError(
                    message=f"OpenAI API connection or server error: {e}",
                    provider="openai",
                    status_code=502,
                    retryable=True
                )

        return self.execute_with_retry("chat_completion", _invoke)

    def analyze_source(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        system_prompt = (
            "You are a civic intelligence analyst. Analyze the following source document and return a JSON object with: "
            "summary (string), detected_language (string, e.g. en, hi, mr), relevance_score (float 0.0-1.0), "
            "contains_civic_complaint (boolean), potential_locations (array of strings)."
        )
        user_content = frame_untrusted_content_for_prompt(source_text)
        raw_json = self._call_chat_completion(system_prompt, user_content)
        try:
            data = json.loads(self.clean_json_response(raw_json))
            data["ai_provider"] = "openai"
            data["ai_model"] = self.model_name
            return data
        except Exception as e:
            logger.error(f"Failed to parse OpenAI analyze_source output: {e}")
            raise ValidationError(f"Invalid JSON returned by OpenAI: {e}")

    def extract_civic_issues(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> List[ExtractedIssueSchema]:
        categories_str = ", ".join(f'"{c}"' for c in CIVIC_CATEGORIES_LIST)
        system_prompt = f"""
You are an expert civic issue extraction engine.
Analyze the source text carefully and extract zero or more civic issues.
Categories must be chosen from: [{categories_str}]. If unsure, use "Other emerging civic concerns".

Return a JSON object with key "issues" containing an array of objects matching this exact schema:
- issue_title: string (concise problem title)
- problem_description: string (factual description)
- category: string (one of the allowed categories)
- subcategory: string (optional detailed subcategory)
- location_mentioned: string (exact text from source, or null)
- normalized_location: string (standardized landmark/street/ward/city)
- latitude: float (only if reliably known, else null)
- longitude: float (only if reliably known, else null)
- affected_population: string (who is affected, mark inferred if not explicit)
- first_reported_date: string (YYYY-MM-DD or null)
- most_recent_observation_date: string (YYYY-MM-DD or null)
- possible_causes: list of strings
- reported_consequences: list of strings
- evidence_excerpts: list of verbatim quotes from the source text
- source_references: list of strings
- confidence_score: float (0.0 to 1.0)
- missing_information: list of strings (what is missing/unverified)
- verification_status: string ("UNVERIFIED", "COMMUNITY_REPORTED", "CORROBORATED")
- suggested_next_steps: list of strings

CRITICAL RULES:
1. Do not invent locations, dates, or causes. Mark uncertain details as "Inferred: ..." or leave null.
2. Separate direct source statements from interpretations.
3. Multilingual text (Hindi, Marathi, English) should be understood while preserving original references.
"""
        user_content = frame_untrusted_content_for_prompt(source_text)
        raw_json = self._call_chat_completion(system_prompt, user_content)

        try:
            parsed = json.loads(self.clean_json_response(raw_json))
            raw_issues = parsed.get("issues", [])
            validated = [ExtractedIssueSchema(**item) for item in raw_issues]
            return validated
        except Exception as e:
            logger.error(f"Validation error in OpenAI extracted issues: {e}")
            raise ValidationError(f"OpenAI extraction schema validation failed: {e}")

    def classify_issue(self, issue_description: str) -> Dict[str, Any]:
        categories_str = ", ".join(f'"{c}"' for c in CIVIC_CATEGORIES_LIST)
        system_prompt = f"""
Classify the civic issue into one category from: [{categories_str}].
Return a JSON object with:
- category: string
- subcategory: string
- confidence: float (0.0 to 1.0)
- reasoning: string
"""
        raw_json = self._call_chat_completion(system_prompt, issue_description)
        try:
            return json.loads(self.clean_json_response(raw_json))
        except Exception as e:
            raise ValidationError(f"Invalid classification output: {e}")

    def find_related_issues(self, target_issue: Dict[str, Any], candidate_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not candidate_issues:
            return []

        system_prompt = """
You are a civic issue deduplication and relationship analyst.
Compare the target issue against candidate issues and classify the relationship between them into one of:
- DUPLICATE_REPORT: The exact same underlying incident reported by another source.
- RECURRING_INCIDENT: Repeated occurrence at the exact same location/facility.
- NEARBY_SIMILAR: Similar problem in a nearby street/neighborhood.
- CROSS_AREA_SIMILAR: Same issue category in a different part of the city.
- UNRELATED_KEYWORD_MATCH: Unrelated issues sharing incidental words.

Return a JSON object with key "matches", containing an array of objects:
- target_issue_id: string
- target_title: string
- relationship_type: string (one of the 5 types above)
- similarity_score: float (0.0 to 1.0)
- match_reasons: list of strings (transparent explanation)
"""
        payload = json.dumps({"target": target_issue, "candidates": candidate_issues})
        raw_json = self._call_chat_completion(system_prompt, payload)
        try:
            parsed = json.loads(self.clean_json_response(raw_json))
            return parsed.get("matches", [])
        except Exception as e:
            raise ValidationError(f"Failed parsing related issues: {e}")

    def identify_stakeholders(self, issue_data: Dict[str, Any], jurisdiction_info: Optional[Dict[str, Any]] = None) -> List[StakeholderRecommendationSchema]:
        system_prompt = """
You are a civic governance expert. Identify the responsible or relevant authorities, municipal departments, and civil society organizations for the issue.
Return a JSON object with key "stakeholders" containing an array of:
- organization_name: string (Official civic body or NGO name)
- department: string (Specific department if applicable)
- relevance_reason: string (Why accountable or helpful)
- jurisdiction_area: string (Geographic jurisdiction, e.g., BMC Ward K-East)
- verification_status: string ("VERIFIED_REGISTRY" or "CANDIDATE_UNVERIFIED")
- confidence_level: float (0.0 to 1.0)
- source_reference: string
- public_portal_or_contact_hint: string (Reference to public portal or helpline, NEVER invent phone numbers or emails)

RULES:
- NEVER invent contact numbers or fake emails.
- If unconfirmed, set verification_status to "CANDIDATE_UNVERIFIED".
"""
        payload = json.dumps({"issue": issue_data, "jurisdiction": jurisdiction_info or {}})
        raw_json = self._call_chat_completion(system_prompt, payload)
        try:
            parsed = json.loads(self.clean_json_response(raw_json))
            return [StakeholderRecommendationSchema(**item) for item in parsed.get("stakeholders", [])]
        except Exception as e:
            raise ValidationError(f"Stakeholder validation failed: {e}")

    def generate_civic_action(self, issue_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> List[CivicActionPlanSchema]:
        system_prompt = """
Generate practical, constructive, safe civic action and volunteer opportunities for citizens.
Activity types allowed: EVIDENCE_COLLECTION, COMMUNITY_SURVEY, OFFICIAL_GRIEVANCE_FILING, AWARENESS_CAMPAIGN, AUTHORIZED_CLEANUP, ACCESSIBILITY_AUDIT, PROGRESS_MONITORING.

Return a JSON object with key "plans", containing an array of objects matching:
- title: string
- problem_summary: string
- why_needed: string
- activity_type: string (one of the allowed activity types)
- step_by_step_plan: list of strings (ordered steps)
- intended_beneficiaries: string
- suggested_roles: list of strings
- required_materials: list of strings
- estimated_effort_hours: float
- suggested_participant_count: int
- potential_collaborators: list of strings
- escalation_channel: string (Official grievance channel)
- expected_outcomes: string
- success_metrics: string
- safety_considerations: list of strings
- prerequisites_and_permissions: list of strings
- is_official_authorization_required: boolean
- safety_risk_level: string ("LOW", "MODERATE", "HIGH_REQUIRES_AUTHORITY")
- ai_confidence: float

SAFETY MANDATE:
- NEVER encourage citizens to confront people, enter moving traffic, handle toxic waste, or perform hazardous electrical/infrastructure repairs.
- For high-safety risks, prioritize official emergency/grievance reporting over citizen intervention.
"""
        payload = json.dumps({"issue": issue_data, "context": context or {}})
        raw_json = self._call_chat_completion(system_prompt, payload)
        try:
            parsed = json.loads(self.clean_json_response(raw_json))
            return [CivicActionPlanSchema(**item) for item in parsed.get("plans", [])]
        except Exception as e:
            raise ValidationError(f"Action plan validation failed: {e}")

    def evaluate_evidence(self, issue_data: Dict[str, Any], evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        system_prompt = """
Evaluate the evidentiary strength, corroboration, and remaining gaps for this civic issue.
Return a JSON object with:
- evidence_count: int
- evidence_strength_score: float (1.0 to 10.0)
- corroboration_level: string
- has_firsthand_quotes: boolean
- has_specific_dates: boolean
- missing_key_factors: list of strings
- verification_recommendation: string
"""
        payload = json.dumps({"issue": issue_data, "evidence": evidence_items})
        raw_json = self._call_chat_completion(system_prompt, payload)
        try:
            return json.loads(self.clean_json_response(raw_json))
        except Exception as e:
            raise ValidationError(f"Evidence evaluation failed: {e}")
