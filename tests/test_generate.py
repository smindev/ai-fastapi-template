import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from main import app  # noqa: E402


class DummyChoice:
    def __init__(self, content: str):
        self.message = type("Msg", (), {"content": content})


class DummyCompletion:
    def __init__(self, content: str):
        self.choices = [DummyChoice(content)]


class DummyChat:
    def __init__(self):
        self.completions = self

    def create(self, model, messages, temperature, max_tokens):
        return DummyCompletion(f"Echo: {messages[0]['content']}")


class DummyOpenAI:
    def __init__(self, api_key=None):
        self.chat = DummyChat()


@pytest.fixture(autouse=True)
def mock_openai():
    with patch("services.ai_service.OpenAI", DummyOpenAI):
        yield


def test_generate_success():
    client = TestClient(app)
    resp = client.post("/generate", json={"prompt": "Hello"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "Echo: Hello" in data["text"]


def test_generate_validation_error():
    client = TestClient(app)
    resp = client.post("/generate", json={"prompt": ""})
    assert resp.status_code == 422
