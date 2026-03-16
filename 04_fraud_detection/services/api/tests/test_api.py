import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

VALID_TRANSACTION = {
    "current_time": "2020-06-21 12:14:25",
    "cc_num": "2703186189652095",
    "trans_num": "2da90c7d74bd46a0caf3777415b3ebd3",
    "merchant": "fraud_Rippin, Kub and Mann",
    "first": "Jennifer",
    "last": "Banks",
    "street": "561 Perry Cove",
    "zip": "48053",
    "city": "Moravian Falls",
    "category": "misc_net",
    "amt": 4.97,
    "gender": "F",
    "state": "NC",
    "city_pop": 3495,
    "lat": 36.0788,
    "long": -81.1781,
    "merch_lat": 36.011293,
    "merch_long": -82.048315,
    "dob": "1988-03-09",
    "job": "Psychologist, counselling",
}


# --- /health ---

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- /predict ---

def _mock_pipeline():
    """Retourne un faux pipeline sklearn."""
    pipeline = MagicMock()
    pipeline.predict.return_value = [0]
    pipeline.predict_proba.return_value = [[0.95, 0.05]]
    return pipeline


@patch("api.utils.fraud_detection_real_time._pipeline", _mock_pipeline())
@patch("api.utils.fraud_detection_real_time._run_id", "test-run-id-1234")
def test_predict_valid_transaction():
    response = client.post("/predict", json=VALID_TRANSACTION)
    assert response.status_code == 200
    data = response.json()
    assert "is_fraud" in data
    assert "fraud_probability" in data
    assert "inference_ms" in data
    assert "run_id" in data
    assert data["is_fraud"] in [0, 1]
    assert 0.0 <= data["fraud_probability"] <= 1.0


@patch("api.utils.fraud_detection_real_time._pipeline", _mock_pipeline())
@patch("api.utils.fraud_detection_real_time._run_id", "test-run-id-1234")
def test_predict_fraud_detected():
    fraud_pipeline = MagicMock()
    fraud_pipeline.predict.return_value = [1]
    fraud_pipeline.predict_proba.return_value = [[0.05, 0.95]]

    with patch("api.utils.fraud_detection_real_time._pipeline", fraud_pipeline):
        response = client.post("/predict", json=VALID_TRANSACTION)
    assert response.status_code == 200
    data = response.json()
    assert data["is_fraud"] == 1
    assert data["fraud_probability"] > 0.5


def test_predict_missing_required_field():
    incomplete = VALID_TRANSACTION.copy()
    del incomplete["amt"]
    response = client.post("/predict", json=incomplete)
    assert response.status_code == 422


def test_predict_empty_body():
    response = client.post("/predict", json={})
    assert response.status_code == 422
