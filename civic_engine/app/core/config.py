"""Configuration management for Civic Issue Discovery & Action Engine."""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "Civic Issue Discovery & Action Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # AI Provider configuration
    # Options: "mock", "openai", "gemini", "anthropic"
    AI_PROVIDER: str = Field(default="mock", description="Active AI provider: mock, openai, gemini, anthropic")
    AI_MODEL: Optional[str] = Field(default=None, description="Model identifier override")

    # Provider API Keys
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API key")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="Anthropic API key")

    # AI execution controls
    REQUEST_TIMEOUT_SECONDS: int = Field(default=30, description="HTTP timeout for AI and scraping requests")
    MAX_RETRIES: int = Field(default=3, description="Retry count for transient API/network errors")
    BACKOFF_FACTOR: float = Field(default=1.5, description="Exponential backoff factor for retries")

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./civic_engine.db",
        description="Database connection string (SQLite or PostgreSQL with pgvector)"
    )

    # Ingestion & Upload security
    FILE_UPLOAD_MAX_BYTES: int = Field(default=10 * 1024 * 1024, description="Max upload size (10 MB)")
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".md", ".csv", ".json", ".xml", ".rss"]

    # Security & API Auth
    API_AUTH_ENABLED: bool = Field(default=False, description="Enable API key protection on mutating endpoints")
    API_SECRET_KEY: Optional[str] = Field(default=None, description="Header API key value for X-API-KEY")

    # Discovery scheduling
    DISCOVERY_ENABLED: bool = Field(default=True, description="Enable proactive discovery loop")
    DISCOVERY_INTERVAL_MINUTES: int = Field(default=60, description="Interval for scheduled discovery")

    # Prioritization weights (normalized 0.0 - 1.0)
    WEIGHT_SEVERITY: float = 0.25
    WEIGHT_COMMUNITY_IMPACT: float = 0.20
    WEIGHT_URGENCY: float = 0.15
    WEIGHT_RECURRENCE: float = 0.15
    WEIGHT_EVIDENCE_STRENGTH: float = 0.15
    WEIGHT_FEASIBILITY: float = 0.10

    @property
    def effective_model(self) -> str:
        """Return the default model name if none is explicitly specified."""
        if self.AI_MODEL:
            return self.AI_MODEL
        defaults = {
            "mock": "mock-civic-analyzer-v1",
            "openai": "gpt-4o-mini",
            "gemini": "gemini-2.5-flash",
            "anthropic": "claude-3-5-sonnet-20241022",
        }
        return defaults.get(self.AI_PROVIDER.lower(), "mock-civic-analyzer-v1")

    def get_safe_status(self) -> dict:
        """Return safe, non-sensitive configuration status."""
        return {
            "project_name": self.PROJECT_NAME,
            "version": self.VERSION,
            "active_provider": self.AI_PROVIDER.lower(),
            "active_model": self.effective_model,
            "providers_configured": {
                "mock": True,
                "openai": bool(self.OPENAI_API_KEY),
                "gemini": bool(self.GEMINI_API_KEY),
                "anthropic": bool(self.ANTHROPIC_API_KEY),
            },
            "database_type": "postgresql" if "postgresql" in self.DATABASE_URL else "sqlite",
            "request_timeout_seconds": self.REQUEST_TIMEOUT_SECONDS,
            "max_retries": self.MAX_RETRIES,
            "api_auth_enabled": self.API_AUTH_ENABLED,
            "discovery_enabled": self.DISCOVERY_ENABLED,
            "discovery_interval_minutes": self.DISCOVERY_INTERVAL_MINUTES,
        }


settings = Settings()
