# LLMWorker

`LLMWorker` is a minimal Python library to centralize LLM operations behind reusable workers.

## Included Components

- `OllamaClient`: low-level client for Ollama HTTP endpoints.
- `TextWorker`: helper class for text generation/chat style requests.
- `ImageWorker`: helper class for image generation requests.


## Basic Usage

```python
from llmworker import OllamaClient, TextWorker, ImageWorker

TEXT_MODEL = "llama3.2:3b"
IMAGE_MODEL = "x/flux2-klein:latest"
OLLAMA_URL = "http://localhost:11434"

client = OllamaClient(base_url=OLLAMA_URL)
text_worker = TextWorker(client, model=TEXT_MODEL)
image_worker = ImageWorker(client, model=IMAGE_MODEL)

answer = text_worker.generate("Explain the origin of universe in one paragraph.")
print(answer)

image_options = {"width": 800, "height": 600}
img_result = image_worker.generate_image("A beach landscape at sunset", **image_options)
with open(f"image.png", "wb") as fw:
    fw.write(img_result)
```
