import pytest
from fastapi.testclient import TestClient

TEST_URL = "/{api_version}/models/{model_name}"
TEST_READY_URL = TEST_URL + "/ready"
TEST_LOAD_URL = TEST_URL + "/load"


@pytest.mark.parametrize("api_version", ["v1", "v2"])
def test_200(api_version, json_model_with_path_kserve_service):
    client = TestClient(json_model_with_path_kserve_service)
    # model is not ready
    response = client.get(
        TEST_READY_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 200
    assert not response.json()
    # load the model
    response = client.post(
        TEST_LOAD_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 200
    assert response.json()
    # model is ready
    response = client.get(
        TEST_READY_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 200
    assert response.json()


@pytest.mark.parametrize("api_version", ["v1", "v2"])
def test_400_registered_with_path_already_loaded(
    api_version,
    json_model_with_path_kserve_service,
):
    client = TestClient(json_model_with_path_kserve_service)
    # model is not ready
    response = client.get(
        TEST_READY_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 200
    assert not response.json()
    # load the model
    response = client.post(
        TEST_LOAD_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 200
    assert response.json()
    # model is ready
    response = client.get(
        TEST_READY_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 200
    assert response.json()
    # load again return 400
    response = client.post(
        TEST_LOAD_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Model already loaded."


@pytest.mark.parametrize("api_version", ["v1", "v2"])
def test_400_registered_with_object_already_loaded(
    api_version,
    json_model_kserve_service,
):
    client = TestClient(json_model_kserve_service)
    # model is ready
    response = client.get(
        TEST_READY_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 200
    assert response.json()
    # load the model return 400
    response = client.post(
        TEST_LOAD_URL.format(api_version=api_version, model_name="json"),
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Model already loaded."


@pytest.mark.parametrize("api_version", ["v1", "v2"])
def test_404(api_version, json_model_with_path_kserve_service):
    client = TestClient(json_model_with_path_kserve_service)
    response = client.post(
        TEST_LOAD_URL.format(api_version=api_version, model_name="invalid"),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found."
