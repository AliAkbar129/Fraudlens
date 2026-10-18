from fastapi.testclient import TestClient
from ml_pipeline.api.main import app

client = TestClient(app)

def test_liveness_does_not_claim_model_readiness():
    assert client.get('/health').json()['model_status'] == 'not_trained'
    assert client.get('/ready').status_code == 503

def test_untrained_model_never_fabricates_predictions():
    for endpoint in ['/predict', '/predict/batch', '/explain/example']:
        result = client.post(endpoint, json={'amount': 100})
        assert result.status_code == 503
        assert 'risk_score' not in result.json()

def test_model_info_has_no_fabricated_metrics():
    assert client.get('/model/info').json()['metrics'] == {}
