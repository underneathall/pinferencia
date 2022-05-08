import pytest
from fastapi.testclient import TestClient

TEST_URL = "/v1/models/{model_name}/versions/{version_name}/ready"


@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_200(
    json_model_default_service,
    version_name,
):
    client = TestClient(json_model_default_service)
    response = client.get(
        TEST_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )
    assert response.status_code == 200
    assert response.json()


def test_404(json_model_default_service):
    client = TestClient(json_model_default_service)
    response = client.get(
        TEST_URL.format(
            model_name="json",
            version_name="invalid",
        )
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found."


@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_200_false(
    json_model_with_path_default_service,
    version_name,
):
    client = TestClient(json_model_with_path_default_service)
    response = client.get(
        TEST_URL.format(
            model_name="json",
            version_name=version_name,
        )
    )

    assert response.status_code == 200
    assert not response.json()
