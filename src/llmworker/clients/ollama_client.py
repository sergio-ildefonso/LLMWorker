"""HTTP client wrapper for Ollama endpoints."""

from __future__ import annotations

from typing import Any, Dict
from urllib.parse import urlparse

import requests
import json

from llmworker.exceptions import OllamaRequestError

DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_TIMEOUT_SECONDS = 150

class OllamaClient:
    """Simple Ollama API client for text and image requests."""

    def __init__(self, base_url: str | None = DEFAULT_OLLAMA_BASE_URL, timeout: int | None = DEFAULT_TIMEOUT_SECONDS, api_url: str | None = None) -> None:
        self.base_url = self._normalize_base_url(base_url or DEFAULT_OLLAMA_BASE_URL)
        self.timeout = timeout or DEFAULT_TIMEOUT_SECONDS
        # If api_url is not provided, build it from base_url.
        if api_url:
            self.api_url = self._normalize_api_url(api_url)
        else:
            self.api_url = f"{self.base_url}/api"

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        normalized = base_url.rstrip("/")
        parsed = urlparse(normalized)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise OllamaRequestError(
                "Invalid base_url. Use a full URL like 'http://localhost:11434'."
            )
        return normalized

    def _normalize_api_url(self, api_url: str) -> str:
        normalized = api_url.rstrip("/")
        if normalized.startswith("http://") or normalized.startswith("https://"):
            return normalized
        if not normalized.startswith("/"):
            normalized = f"/{normalized}"
        return f"{self.base_url}{normalized}"

    def _generate(self, model: str, prompt: str, stream: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Generate a response from Ollama
        
        Args:
            model: Name of the model to use (example: 'llama3.2:3b', 'x/flux2-klein:latest', etc.)
            prompt: The prompt to send to the model
            stream: Whether to stream the response (default: False)
            **kwargs: Additional parameters (temperature, top_p, etc.)
        
        Returns:
            Dictionary containing the response
        """
        url = f"{self.api_url}/generate"        
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            if stream:
                # Handle streaming response
                result = {"response": ""}
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            result["response"] += chunk["response"]
                            print(chunk["response"], end="", flush=True)
                        if chunk.get("done", False):
                            result.update(chunk)
                            break
                print()  # New line after streaming
                return result
            else:
                return response.json()
        
        except requests.exceptions.ConnectionError as exc:
            raise OllamaRequestError(
                f"Could not connect to Ollama at {self.base_url}. Make sure Ollama is running."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise OllamaRequestError(
                "Request timed out. The model might be taking too long to respond."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            error_detail = ""
            if exc.response is not None:
                try:
                    payload = exc.response.json()
                    error_detail = str(payload.get("error") or payload)
                except ValueError:
                    error_detail = exc.response.text.strip()
            detail_suffix = f" | details: {error_detail}" if error_detail else ""
            raise OllamaRequestError(
                f"HTTP error in generate request: {exc}{detail_suffix}"
            ) from exc

    def generate_text(self, model: str, prompt: str, stream: bool = False, **kwargs: Any) -> dict[str, Any]:
        """
        Generate text using Ollama
        
        Args:
            model: Name of the model to use
            prompt: The prompt to send to the model
            stream: Whether to stream the response (default: False)
            **kwargs: Additional parameters
        """
        return self._generate(model=model, prompt=prompt, stream=stream, **kwargs)

    def generate_image(self, model: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        """
        Generate image using Ollama
        
        Args:
            model: Name of the model to use
            prompt: The prompt to send to the model
            **kwargs: Additional parameters
        
        Returns:
            Dictionary containing the response
        """
        return self._generate(model=model, prompt=prompt, **kwargs)

    def chat(self, model: str, messages: list, stream: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Chat with Ollama using a conversation format
        
        Args:
            model: Name of the model to use
            messages: List of message dictionaries with 'role' and 'content' keys
                     Example: [{"role": "user", "content": "Hello!"}]
            stream: Whether to stream the response (default: False)
            **kwargs: Additional parameters
        
        Returns:
            Dictionary containing the response
        """
        url = f"{self.api_url}/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            if stream:
                result = {"message": {"content": ""}}
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            content = chunk["message"]["content"]
                            result["message"]["content"] += content                            
                        if chunk.get("done", False):
                            result.update(chunk)
                            break                
                return result
            else:
                return response.json()
        
        except requests.exceptions.ConnectionError as exc:
            raise OllamaRequestError(
                f"Chat error connecting to Ollama at {self.base_url}. Make sure Ollama is running."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise OllamaRequestError(
                "Chat timeout error: The model might be taking too long to respond."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            error_detail = ""
            if exc.response is not None:
                try:
                    payload = exc.response.json()
                    error_detail = str(payload.get("error") or payload)
                except ValueError:
                    error_detail = exc.response.text.strip()
            detail_suffix = f" | details: {error_detail}" if error_detail else ""
            raise OllamaRequestError(
                f"HTTP error in chat request: {exc}{detail_suffix}"
            ) from exc
    
    def list_models(self) -> list:
        """
        List all available models in Ollama
        
        Returns:
            List of available models
        """
        url = f"{self.api_url}/tags"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
        except requests.exceptions.ConnectionError as exc:
            raise OllamaRequestError(
                f"Error connecting to Ollama at {self.base_url}. Make sure Ollama is running."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise OllamaRequestError("List models request timed out.") from exc
        except requests.exceptions.HTTPError as exc:
            error_detail = ""
            if exc.response is not None:
                try:
                    payload = exc.response.json()
                    error_detail = str(payload.get("error") or payload)
                except ValueError:
                    error_detail = exc.response.text.strip()
            detail_suffix = f" | details: {error_detail}" if error_detail else ""
            raise OllamaRequestError(
                f"HTTP error in list models request: {exc}{detail_suffix}"
            ) from exc
