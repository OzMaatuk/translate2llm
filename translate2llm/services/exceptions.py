"""Custom exceptions for the application."""

class TranslationError(Exception):
    """Raised when a translation operation fails."""
    pass

class LLMError(Exception):
    """Raised when an LLM operation fails."""
    pass

class ConfigurationError(Exception):
    """Raised when there is a configuration error."""
    pass