from fastapi.testclient import TestClient

TEST_URL = "/v1/models/{model_name}"
TEST_READY_URL = TEST_URL + "/ready"
TEST_LOAD_URL = TEST_URL + "/load"


def test_200(json_model_with_path_default_service):
    client = TestClient(json_model_with_path_default_service)
    # model is not ready
    response = client.get(TEST_READY_URL.format(model_name="json"))
    assert response.status_code == 200
    assert not response.json()
    # load the model
    response = client.post(TEST_LOAD_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json()
    # model is ready
    response = client.get(TEST_READY_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json()


def test_400_registered_with_path_already_loaded(
    json_model_with_path_default_service,
):
    client = TestClient(json_model_with_path_default_service)
    # model is not ready
    response = client.get(TEST_READY_URL.format(model_name="json"))
    assert response.status_code == 200
    assert not response.json()
    # load the model
    response = client.post(TEST_LOAD_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json()
    # model is ready
    response = client.get(TEST_READY_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json()
    # load again return 400
    response = client.post(TEST_LOAD_URL.format(model_name="json"))
    assert response.status_code == 400
    assert response.json()["detail"] == "Model already loaded."


def test_400_registered_with_object_already_loaded(
    json_model_default_service,
):
    client = TestClient(json_model_default_service)
    # model is ready
    response = client.get(TEST_READY_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json()
    # load the model return 400
    response = client.post(TEST_LOAD_URL.format(model_name="json"))
    assert response.status_code == 400
    assert response.json()["detail"] == "Model already loaded."


def test_404(json_model_with_path_default_service):
    client = TestClient(json_model_with_path_default_service)
    response = client.post(TEST_LOAD_URL.format(model_name="invalid"))
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found."
