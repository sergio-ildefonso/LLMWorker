from llmworker import ImageWorker, OllamaClient, TextWorker


def test_exports() -> None:
    client = OllamaClient()
    assert isinstance(TextWorker(client=client, model="llama3.2"), TextWorker)
    assert isinstance(ImageWorker(client=client, model="sdxl"), ImageWorker)
