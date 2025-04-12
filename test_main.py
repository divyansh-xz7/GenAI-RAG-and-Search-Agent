# test_main.py
# import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    user_data = {"name": "test_user"}
    response = client.post("/create-user", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == "test_user"

def test_fetch_sessions():
    user_id = 1
    response = client.get(f"/fetch-sessions/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_session():
    session_data = {"user_id": 1}
    response = client.post("/create-session", json=session_data)
    assert response.status_code == 200
    assert response.json()["user_id"] == 1

def test_get_session_history():
    session_id = 1
    response = client.get(f"/get-session-history/{session_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0

