"""Custom exceptions for llmworker."""


class LLMWorkerError(Exception):
    """Base exception for all library errors."""


class OllamaRequestError(LLMWorkerError):
    """Raised when an Ollama request fails."""
