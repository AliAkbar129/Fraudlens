import pytest
from fastapi.testclient import TestClient
from ml_pipeline.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint_valid_input():
    payload = {
        "transaction_id": "tx123",
        "amount": 100.50,
        "card_id": "c456",
        "time_step": 1234567890
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "risk_score" in response.json()

def test_predict_invalid_input_returns_422():
    payload = {
        "transaction_id": "tx123",
        "amount": -10, # Invalid amount
        "card_id": "c456",
        "time_step": 1234567890
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_batch_predict():
    payload = {
        "transactions": [
            {
                "transaction_id": "tx1",
                "amount": 100,
                "card_id": "c1",
                "time_step": 1
            },
            {
                "transaction_id": "tx2",
                "amount": 200,
                "card_id": "c2",
                "time_step": 2
            }
        ]
    }
    response = client.post("/predict/batch", json=payload)
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 2

def test_model_info():
    response = client.get("/model/info")
    assert response.status_code == 200
    assert "version" in response.json()
