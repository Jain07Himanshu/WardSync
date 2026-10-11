"""Custom exception hierarchy for the Civic Issue Discovery & Action Engine."""


class CivicEngineError(Exception):
    """Base exception for all civic engine errors."""
    pass


class ConfigurationError(CivicEngineError):
    """Raised when required configuration or API credentials are missing or invalid."""
    pass


class ProviderError(CivicEngineError):
    """Raised when an external AI provider fails or returns an unrecoverable error."""
    def __init__(self, message: str, provider: str, status_code: int = 502, retryable: bool = False):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code
        self.retryable = retryable


class IngestionError(CivicEngineError):
    """Raised when parsing or ingesting a document fails."""
    pass


class UnsupportedFileTypeError(IngestionError):
    """Raised when an uploaded file type is not supported."""
    pass


class PromptInjectionDetectedError(CivicEngineError):
    """Raised when suspicious prompt injection patterns are identified in source text."""
    pass


class ValidationError(CivicEngineError):
    """Raised when structured AI output does not match required schemas."""
    pass


class ResourceNotFoundError(CivicEngineError):
    """Raised when a requested resource is not found."""
    pass
