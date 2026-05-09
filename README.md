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
Don't forget to check / change the project version on pyproject.toml. (example:)

```
version = "<put the version here>"
```

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
text_worker = TextWorker(client, model="llama3.2:3b")
image_worker = ImageWorker(client, model="x/flux2-klein:latest")

answer = text_worker.generate("Explain the origin of universe in one paragraph.")
print(answer)

Example image generation (model must support images)
img_result = image_worker.generate_image("A futuristic city at sunset")
print(img_result)
```


## PIP install from GitHub
To install directly from GitHub, use the following command 
```bash
pip install "git+https://github.com/sergio-ildefonso/LLMWorker.git@v0.1.7"
```

## Important
Note: In some Ollama versions (probably, greater than 0.23.0), Ollama is not working stable with image models. 
It is adviseable to remove the unstable version of Ollama and install a stable version, in example: 0.23.0
Here are the steps to do it:

---

**a) Uninstall Ollama:**  

1. **Close the application**
    ```bash
    killall Ollama
    ```

2. **Remove the application and executable**
    ```bash
    sudo rm -rf /Applications/Ollama.app
    sudo rm /usr/local/bin/ollama
    ```

3. **Clear cache and support data**
    ```bash
    rm -rf ~/Library/Application\ Support/Ollama
    rm -rf ~/Library/Caches/com.electron.ollama
    rm -rf ~/Library/Saved\ Application\ State/com.electron.ollama.savedState
    ```

4. **(Optional) Delete downloaded templates**
    ```bash
    rm -rf ~/.ollama
    ```

---

**b) Install Ollama Version 0.23.0:**  

1. **Download the official Ollama binary**
    ```bash
    curl -L -o Ollama-darwin.zip https://github.com/ollama/ollama/releases/download/v0.23.0/Ollama-darwin.zip
    ```
    (Or download manually from [Ollama Releases](https://github.com/ollama/ollama/releases/))

2. **Unzip into the Applications folder**
    ```bash
    unzip Ollama-darwin.zip -d /Applications/
    ```
    (Or unzip and move the app to `/Applications` manually.)

3. **Delete the zip file to save disk space**
    ```bash
    rm Ollama-darwin.zip
    ```

4. **Create a global symlink for the `ollama` command**
    ```bash
    sudo ln -sf /Applications/Ollama.app/Contents/Resources/ollama /usr/local/bin/ollama
    ```

5. **Remove macOS quarantine on the app**
    ```bash
    xattr -r -d com.apple.quarantine /Applications/Ollama.app
    ```