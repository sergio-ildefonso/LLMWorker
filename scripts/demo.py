"""Quick demo for llmworker package usage."""

from llmworker import ImageWorker, OllamaClient, TextWorker

import time


def main() -> None:
    client = OllamaClient(base_url="http://localhost:11434")

    # Text generation
    start_time = time.time()
    text_worker = TextWorker(client=client, model="llama3.2:3b") # example: llama3.2:3b
    text_response = text_worker.generate("Write a short greeting for a Python library user.")
    print("Text response:\\n", text_response)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

    # Image generation - base64
    image_worker = ImageWorker(client=client, model="x/flux2-klein:latest") # example: x/flux2-klein:latest
    start_time = time.time()
    options={
        "width": 512,
        "height": 512
    }
    image_response = image_worker.generate_image_base64("An open book with a green cover", **options)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    # Uncomment to print the base64 string
    # print("Image base64 response:\\n", image_response)

    # Image generation - bytes
    start_time = time.time()
    options={
        "width": 512,
        "height": 512
    }
    image_response = image_worker.generate_image("A robotic assistant in front of a laptop, smiling to the viewer", **options) # example: x/flux2-klein:latest
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    # Uncomment to save the image in a file
    # if image_response:
    #     with open("image.png", "wb") as f:
    #         f.write(image_response)
    #     print("Image saved to image.png")
    print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
