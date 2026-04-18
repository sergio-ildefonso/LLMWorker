# LLMWorker

`LLMWorker` is a minimal Python library to centralize LLM operations behind reusable workers.

## Included Components

- `OllamaClient`: low-level client for Ollama HTTP endpoints.
- `TextWorker`: helper class for text generation/chat style requests.
- `ImageWorker`: helper class for image generation requests.

## Quick Start 
Attention: Need to have Ollama running with the selected models

```bash
bash scripts/bootstrap.sh
python scripts/demo.py
```


## Basic Usage

```python
from llmworker import OllamaClient, TextWorker, ImageWorker

client = OllamaClient(base_url="http://localhost:11434")
text_worker = TextWorker(client, model="llama3.2:3b")
image_worker = ImageWorker(client, model="x/flux2-klein:latest")

answer = text_worker.generate("Explain the origin of universe in one paragraph.")
print(answer)

Example image generation (model must support images)
img_result = image_worker.generate_image("A futuristic city at sunset")
print(img_result)
```
