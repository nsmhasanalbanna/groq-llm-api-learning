import pytest
from fastapi.testclient import TestClient

from main import app
from clients.groq_client import get_groq_client
from clients.fake_groq_client import get_fake_groq_client


@pytest.fixture
def client():
    app.dependency_overrides[get_groq_client] = get_fake_groq_client

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_groq_client, None)


def test_ai_question(client):
    response = client.post(
        "/ai/question/",
        json={
            "question": "llm and gpu relationship",
            "max_tokens": 100,
            "temperature": 0.2
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "question": "llm and gpu relationship",
        "answer": "Fake AI Response"
    }

def test_ai_question_invalid_max_tokens(client):
    response = client.post(
        "/ai/question/",
        json={
            "question": "llm and gpu relationship",
            "max_tokens": 500,
            "temperature": 0.2
        }
    )

    assert response.status_code == 422