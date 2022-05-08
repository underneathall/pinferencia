import pytest
from fastapi.testclient import TestClient

TEST_URL = "/v1/models/{model_name}/versions/{version_name}"
TEST_READY_URL = TEST_URL + "/ready"
TEST_LOAD_URL = TEST_URL + "/load"


@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_200(
    json_model_with_path_default_service,
    version_name,
):
    client = TestClient(json_model_with_path_default_service)
    response = client.get(
        TEST_READY_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert not response.json()
    response = client.post(
        TEST_LOAD_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert response.json()
    response = client.get(
        TEST_READY_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert response.json()


@pytest.mark.parametrize("version_name", ["loaded"])
def test_400_registered_with_path_already_loaded(
    json_model_with_path_default_service,
    version_name,
):
    client = TestClient(json_model_with_path_default_service)
    response = client.get(
        TEST_READY_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert response.json()
    response = client.post(
        TEST_LOAD_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Model already loaded."


@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_400_registered_with_object_already_loaded(
    json_model_default_service,
    version_name,
):
    client = TestClient(json_model_default_service)
    response = client.get(
        TEST_READY_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert response.json()
    response = client.post(
        TEST_LOAD_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Model already loaded."


@pytest.mark.parametrize("version_name", ["invalid"])
def test_404(
    json_model_with_path_default_service,
    version_name,
):
    client = TestClient(json_model_with_path_default_service)
    response = client.post(
        TEST_LOAD_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found."
