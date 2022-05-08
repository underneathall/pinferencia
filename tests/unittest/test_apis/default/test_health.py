from fastapi.testclient import TestClient

TEST_URL = "/v1/healthz"


def test_200(json_model_default_service):
    client = TestClient(json_model_default_service)
    response = client.get(TEST_URL)
    assert response.status_code == 200
    assert response.json()
