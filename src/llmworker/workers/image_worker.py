"""Image worker that uses the Ollama client."""

from __future__ import annotations

from typing import Any

from llmworker.clients.ollama_client import OllamaClient


class ImageWorker:
    """High-level image utility for prompt-based generation."""

    def __init__(self, client: OllamaClient, model: str) -> None:
        self.client = client
        self.model = model

    def generate_image(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        """Generate image data and return the full response payload."""
        return self.client.generate_image(model=self.model, prompt=prompt, **kwargs)
