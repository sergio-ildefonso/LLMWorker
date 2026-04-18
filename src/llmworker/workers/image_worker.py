"""Image worker that uses the Ollama client."""

from __future__ import annotations

from typing import Any

from llmworker.clients.ollama_client import OllamaClient
import base64


class ImageWorker:
    """High-level image utility for prompt-based generation."""

    def __init__(self, client: OllamaClient, model: str) -> None:
        self.client = client
        self.model = model

    def generate_image(self, prompt: str, **kwargs: Any) -> bytes | None:
        """Generate image data and return the image bytes."""
        response = self.client.generate_image(model=self.model, prompt=prompt, **kwargs)
        image_b64 = response.get("image") or response.get("images", [None])[0]
        if not image_b64:
            raise ValueError(f"No image data in response: {response}")
        img_bytes = base64.b64decode(image_b64)
        return img_bytes
    
    def generate_image_base64(self, prompt: str, **kwargs: Any) -> str | None:
        """Generate image data and return the image base64 string."""
        response = self.client.generate_image(model=self.model, prompt=prompt, **kwargs)
        image_b64 = response.get("image") or response.get("images", [None])[0]
        if not image_b64:
            raise ValueError(f"No image data in response: {response}")
        return image_b64
