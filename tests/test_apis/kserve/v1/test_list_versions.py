from fastapi.testclient import TestClient

TEST_URL = "/v1/models/{model_name}"


def test_get_json_model_versions(json_model_kserve_service):
    client = TestClient(json_model_kserve_service)
    response = client.get(TEST_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json() == [
        {"name": "default", "platform": ""},
        {"name": "v1", "platform": ""},
    ]