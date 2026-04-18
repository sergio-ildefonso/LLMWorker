"""Quick demo for llmworker package usage."""

from llmworker import ImageWorker, OllamaClient, TextWorker


def main() -> None:
    client = OllamaClient(base_url="http://localhost:11434")

    text_worker = TextWorker(client=client, model="llama3.2")
    text_response = text_worker.generate("Write a short greeting for a Python library user.")
    print("Text response:\\n", text_response)

    # Uncomment and adjust model for image-capable endpoint support.
    # image_worker = ImageWorker(client=client, model="sdxl")
    # image_response = image_worker.generate_image("A robotic assistant coding at night")
    # print("Image response:\\n", image_response)


if __name__ == "__main__":
    main()
