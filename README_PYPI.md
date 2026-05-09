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