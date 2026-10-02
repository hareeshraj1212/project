from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation_rejects_empty_question():
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422
