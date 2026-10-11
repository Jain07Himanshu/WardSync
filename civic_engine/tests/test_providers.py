"""Tests for AI provider abstraction, factory, switching, and error handling."""

import pytest
from app.core.config import settings
from app.core.exceptions import ConfigurationError
from app.providers.factory import get_ai_provider
from app.providers.mock_provider import MockAIProvider
from app.schemas.issue import ExtractedIssueSchema
from app.schemas.stakeholder import StakeholderRecommendationSchema
from app.schemas.opportunity import CivicActionPlanSchema


def test_provider_factory_mock():
    provider = get_ai_provider("mock")
    assert isinstance(provider, MockAIProvider)
    assert provider.provider_name == "mock"


def test_provider_factory_missing_keys(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    with pytest.raises(ConfigurationError) as exc_info:
        get_ai_provider("gemini")
    assert "GEMINI_API_KEY is not configured" in str(exc_info.value)

    monkeypatch.setattr(settings, "ANTHROPIC_API_KEY", "")
    with pytest.raises(ConfigurationError) as exc_info:
        get_ai_provider("anthropic")
    assert "ANTHROPIC_API_KEY is not configured" in str(exc_info.value)


def test_mock_provider_extract_civic_issues():
    provider = MockAIProvider()
    text = "Large 8-inch pothole on S.V. Road near Andheri station causing accidents."
    issues = provider.extract_civic_issues(text)
    assert len(issues) >= 1
    issue = issues[0]
    assert isinstance(issue, ExtractedIssueSchema)
    assert "Pothole" in issue.issue_title
    assert issue.category == "Roads and potholes"
    assert issue.normalized_location is not None
    assert issue.confidence_score > 0.8


def test_mock_provider_camel_case_aliases():
    provider = MockAIProvider()
    text = "Clogged drain and waterlogging at Milan Subway."
    issues = provider.extractCivicIssues(text)
    assert len(issues) >= 1
    assert "Drainage and waterlogging" in issues[0].category

    classified = provider.classifyIssue("potholes on highway")
    assert classified["category"] == "Roads and potholes"


def test_mock_provider_stakeholder_and_actions():
    provider = MockAIProvider()
    issue_data = {
        "title": "Severe road damage",
        "category": "Roads and potholes",
        "normalized_location": "S.V. Road, Andheri West, Mumbai",
    }
    stakeholders = provider.identify_stakeholders(issue_data)
    assert len(stakeholders) >= 1
    assert any("BMC" in s.organization_name or "Brihanmumbai" in s.organization_name for s in stakeholders)

    actions = provider.generate_civic_action(issue_data)
    assert len(actions) >= 1
    assert isinstance(actions[0], CivicActionPlanSchema)
    assert actions[0].safety_risk_level == "LOW"
    assert len(actions[0].step_by_step_plan) >= 3
