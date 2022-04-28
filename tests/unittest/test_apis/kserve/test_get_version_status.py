import pytest
from fastapi.testclient import TestClient

TEST_URL = "/{api_version}/models/{model_name}/versions/{version_name}/ready"


@pytest.mark.parametrize("api_version", ["v1", "v2"])
@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_200(
    api_version,
    json_model_kserve_service,
    version_name,
):
    client = TestClient(json_model_kserve_service)
    response = client.get(
        TEST_URL.format(
            api_version=api_version,
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert response.json()


@pytest.mark.parametrize("api_version", ["v1", "v2"])
def test_404(json_model_kserve_service, api_version):
    client = TestClient(json_model_kserve_service)
    response = client.get(
        TEST_URL.format(
            api_version=api_version,
            model_name="json",
            version_name="invalid",
        )
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found."


@pytest.mark.parametrize("api_version", ["v1", "v2"])
@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_200_false(
    api_version,
    json_model_with_path_kserve_service,
    version_name,
):
    client = TestClient(json_model_with_path_kserve_service)
    response = client.get(
        TEST_URL.format(
            api_version=api_version,
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert not response.json()


@pytest.mark.parametrize("api_version", ["v1", "v2"])
@pytest.mark.parametrize("version_name", ["loaded"])
def test_200_with_path_loaded_true(
    api_version,
    json_model_with_path_kserve_service,
    version_name,
):
    client = TestClient(json_model_with_path_kserve_service)
    response = client.get(
        TEST_URL.format(
            api_version=api_version,
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert response.json()
