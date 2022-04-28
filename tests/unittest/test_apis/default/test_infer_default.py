import pytest
from fastapi.testclient import TestClient

from .data import inference_data

TEST_URL = "/v1/models/{model_name}/predict"


@pytest.mark.parametrize("inference_data", inference_data)
def test_200_json_model(
    json_model_default_service,
    inference_data,
):
    client = TestClient(json_model_default_service)
    response = client.post(
        TEST_URL.format(model_name="json"), json=inference_data["request"]
    )
    assert response.status_code == 200
    assert response.json()["data"] == inference_data["response"]["data"]
