"""Text worker that uses the Ollama client."""

from __future__ import annotations

from typing import Any

from llmworker.clients.ollama_client import OllamaClient


class TextWorker:
    """High-level text utility for prompt-based generation."""

    def __init__(self, client: OllamaClient, model: str) -> None:
        self.client = client
        self.model = model

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate text and return only the response string."""
        raw = self.client.generate_text(model=self.model, prompt=prompt, **kwargs)
        return str(raw.get("response", ""))

    def generate_raw(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        """Generate text and return the full Ollama response payload."""
        return self.client.generate_text(model=self.model, prompt=prompt, **kwargs)
