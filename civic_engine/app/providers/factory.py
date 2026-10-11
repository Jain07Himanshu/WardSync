"""Provider factory to instantiate and switch AI providers dynamically."""

import logging
from typing import Optional

from app.core.config import settings
from app.core.exceptions import ConfigurationError
from app.providers.base import BaseAIProvider
from app.providers.mock_provider import MockAIProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.anthropic_provider import AnthropicProvider

logger = logging.getLogger(__name__)


def get_ai_provider(provider_name: Optional[str] = None, model_name: Optional[str] = None) -> BaseAIProvider:
    """
    Factory function to retrieve the configured AI provider instance.

    Raises ConfigurationError if the requested provider's credentials are not present.
    Never fabricates a successful connection if keys are missing.
    """
    selected = (provider_name or settings.AI_PROVIDER or "mock").strip().lower()

    if selected == "mock":
        logger.info("Using deterministic Mock AI Provider.")
        return MockAIProvider(model_name=model_name or settings.effective_model)

    elif selected == "openai":
        if not settings.OPENAI_API_KEY or not settings.OPENAI_API_KEY.strip():
            raise ConfigurationError(
                "AI Provider is set to 'openai', but OPENAI_API_KEY is not configured. "
                "Set OPENAI_API_KEY in .env or switch to AI_PROVIDER=mock for offline development."
            )
        logger.info(f"Instantiating OpenAI Provider with model: {model_name or settings.effective_model}")
        return OpenAIProvider(model_name=model_name or settings.effective_model)

    elif selected == "gemini":
        if not settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY.strip():
            raise ConfigurationError(
                "AI Provider is set to 'gemini', but GEMINI_API_KEY is not configured. "
                "Set GEMINI_API_KEY in .env or switch to AI_PROVIDER=mock for offline development."
            )
        logger.info(f"Instantiating Gemini Provider with model: {model_name or settings.effective_model}")
        return GeminiProvider(model_name=model_name or settings.effective_model)

    elif selected == "anthropic":
        if not settings.ANTHROPIC_API_KEY or not settings.ANTHROPIC_API_KEY.strip():
            raise ConfigurationError(
                "AI Provider is set to 'anthropic', but ANTHROPIC_API_KEY is not configured. "
                "Set ANTHROPIC_API_KEY in .env or switch to AI_PROVIDER=mock for offline development."
            )
        logger.info(f"Instantiating Anthropic Provider with model: {model_name or settings.effective_model}")
        return AnthropicProvider(model_name=model_name or settings.effective_model)

    else:
        raise ConfigurationError(
            f"Unsupported AI Provider '{selected}'. Supported providers are: 'mock', 'openai', 'gemini', 'anthropic'."
        )
