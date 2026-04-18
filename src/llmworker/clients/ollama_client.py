"""HTTP client wrapper for Ollama endpoints."""

from __future__ import annotations

from typing import Any

import requests

from llmworker.config import DEFAULT_OLLAMA_BASE_URL, DEFAULT_TIMEOUT_SECONDS
from llmworker.exceptions import OllamaRequestError


class OllamaClient:
    """Simple Ollama API client for text and image requests."""

    def __init__(
        self,
        base_url: str = DEFAULT_OLLAMA_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate_text(self, model: str, prompt: str, stream: bool = False, **kwargs: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **kwargs,
        }
        return self._post("/api/generate", payload)

    def generate_image(self, model: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            **kwargs,
        }
        return self._post("/api/images", payload)

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise OllamaRequestError(f"Request to '{url}' failed: {exc}") from exc
