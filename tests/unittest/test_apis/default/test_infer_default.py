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


@pytest.mark.parametrize(
    "inference_data",
    [
        {
            "request": {"data": "a"},
            "response": {"data": "a"},
        },
        {
            "request": {"data": 1},
            "response": {"data": "1"},
        },
        {
            "request": {"data": True},
            "response": {"data": "True"},
        },
    ],
)
@pytest.mark.parametrize("register_with_decorator", [True, False])
def test_200_dummy_model(
    inference_data,
    register_with_decorator,
    dummy_model_service,
    dummy_model_service_with_decorator,
):
    if register_with_decorator:
        client = TestClient(dummy_model_service_with_decorator)
    else:
        client = TestClient(dummy_model_service)
    response = client.post(
        TEST_URL.format(model_name="dummy"),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert response.json()["data"] == inference_data["response"]["data"]


@pytest.mark.parametrize(
    "inference_data",
    [
        {"request": {"data": {"a": 1}}},
        {"request": {"data": [1, 2]}},
    ],
)
@pytest.mark.parametrize("register_with_decorator", [True, False])
def test_422_dummy_model(
    inference_data,
    register_with_decorator,
    dummy_model_service,
    dummy_model_service_with_decorator,
):
    if register_with_decorator:
        client = TestClient(dummy_model_service_with_decorator)
    else:
        client = TestClient(dummy_model_service)
    response = client.post(
        TEST_URL.format(model_name="dummy"),
        json=inference_data["request"],
    )
    assert response.status_code == 422
