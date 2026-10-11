import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable auto-discovery."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Google Gemini Configuration
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"
    EMBEDDING_MODEL: str = "text-embedding-004"

    # Supabase Configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None

    # Pipeline Tuning Constants
    SIMILARITY_THRESHOLD: float = 0.82
    VERIFICATION_THRESHOLD: int = 65
    MATCH_LIMIT: int = 5

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"

    @property
    def is_supabase_configured(self) -> bool:
        return bool(self.SUPABASE_URL and self.SUPABASE_KEY and "your-project-ref" not in self.SUPABASE_URL)

    @property
    def is_gemini_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY and "your_gemini_api_key" not in self.GEMINI_API_KEY)


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
