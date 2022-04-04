from fastapi.testclient import TestClient

TEST_URL = "/v1/models/{model_name}/ready"


def test_200(json_model_default_service):
    client = TestClient(json_model_default_service)
    response = client.get(TEST_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json()


def test_404(json_model_default_service):
    client = TestClient(json_model_default_service)
    response = client.get(TEST_URL.format(model_name="invalid"))
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found."


def test_200_false(json_model_with_path_default_service):
    client = TestClient(json_model_with_path_default_service)
    response = client.get(TEST_URL.format(model_name="json"))
    assert response.status_code == 200
    assert not response.json()
