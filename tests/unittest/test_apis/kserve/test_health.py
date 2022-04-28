import pytest
from fastapi.testclient import TestClient

TEST_URL = "/{api_version}/healthz"


@pytest.mark.parametrize("api_version", ["v1", "v2"])
def test_200(json_model_kserve_service, api_version):
    client = TestClient(json_model_kserve_service)
    response = client.get(TEST_URL.format(api_version=api_version))
    assert response.status_code == 200
    assert response.json()
