import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.api.v1.routes.run_agent", new_callable=AsyncMock)
def test_analyze_topic_endpoint(mock_run_agent):
    # Mock the agent response
    mock_run_agent.return_value = "Mocked Newsletter Content"
    
    # Test valid request
    response = client.post(
        "/api/v1/analyze",
        json={"topic": "Artificial Intelligence"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"newsletter": "Mocked Newsletter Content"}
    mock_run_agent.assert_called_once_with("Artificial Intelligence")

def test_analyze_topic_empty_body():
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 422  # Pydantic validation error

def test_analyze_topic_empty_topic():
    response = client.post("/api/v1/analyze", json={"topic": "  "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Topic cannot be empty"
