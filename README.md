# LLMWorker

`LLMWorker` is a minimal Python library to centralize LLM operations behind reusable workers.

## Included Components

- `OllamaClient`: low-level client for Ollama HTTP endpoints.
- `TextWorker`: helper class for text generation/chat style requests.
- `ImageWorker`: helper class for image generation requests.

## Quick Start

```bash
bash scripts/bootstrap.sh
python scripts/demo.py
```

## Build Package

```bash
bash scripts/build.sh
```

## Check Package Name (PyPI)

Before publishing, validate that your package name is free:

```bash
python scripts/check_name.py llmworker
```

If it is taken, choose a new name (for example `llmworker-sergio`) and update it in `pyproject.toml`.

## Install As A Package

Install from source (non-editable):

```bash
pip install .
```

Install from wheel artifact:

```bash
bash scripts/build.sh
pip install dist/*.whl
```

Install from PyPI (after you publish):

```bash
pip install llmworker
```

## Install (editable)

```bash
pip install -e .
```

## Publish To PyPI

```bash
bash scripts/publish.sh
```

Recommended release flow:

```bash
python scripts/check_name.py llmworker
bash scripts/build.sh
bash scripts/publish.sh
```

## Basic Usage

```python
from llmworker import OllamaClient, TextWorker, ImageWorker

client = OllamaClient(base_url="http://localhost:11434")
text_worker = TextWorker(client, model="llama3.2")
image_worker = ImageWorker(client, model="sdxl")

answer = text_worker.generate("Explain transformers in one paragraph.")
print(answer)

# Example image generation (model must support images)
# img_result = image_worker.generate_image("A futuristic city at sunset")
# print(img_result)
```
