import copy

import pytest
from fastapi.testclient import TestClient

from .data import json_inference_data, sum_prod_inference_data

BASE_URL = "/v2/models/{model_name}"
TEST_PREDICT_URL = BASE_URL + "/infer"
TEST_READY_URL = BASE_URL + "/ready"
TEST_LOAD_URL = BASE_URL + "/load"


@pytest.mark.parametrize("inference_data", json_inference_data)
def test_200_json_model(
    json_model_kserve_service,
    inference_data,
):
    client = TestClient(json_model_kserve_service)
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json"),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert (
        response.json()["outputs"][0]["data"]
        == inference_data["response"]["outputs"][0]["data"]
    )


@pytest.mark.parametrize("inference_data", sum_prod_inference_data)
def test_200_sum_product_model(
    sum_product_model_kserve_service,
    inference_data,
):
    client = TestClient(sum_product_model_kserve_service)
    response = client.post(
        TEST_PREDICT_URL.format(model_name="sum_prod"),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert isinstance(response.json()["outputs"], list)
    test_inference_data = copy.deepcopy(inference_data)
    for output in response.json()["outputs"]:
        assert output["data"] == test_inference_data["response"][
            "outputs"
        ].pop(output["name"])
    assert not test_inference_data["response"]["outputs"]


@pytest.mark.parametrize("inference_data", sum_prod_inference_data)
def test_200_sum_product_model_partial_outputs(
    sum_product_model_kserve_v2_partial_output_service,
    inference_data,
):
    client = TestClient(sum_product_model_kserve_v2_partial_output_service)
    response = client.post(
        TEST_PREDICT_URL.format(model_name="sum_prod"),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert isinstance(response.json()["outputs"], list)
    test_inference_data = copy.deepcopy(inference_data)
    for output in response.json()["outputs"]:
        assert output["data"] == test_inference_data["response"][
            "outputs"
        ].pop(output["name"])
    assert not test_inference_data["response"]["outputs"]


@pytest.mark.parametrize(
    "data",
    [
        {
            "input": {"inputs": [{"data": 1}, {"data": 2}]},
            "message": "Input name should be provided given multiple inputs",
        },
        {
            "input": {"inputs": {"data": 1}},
            "message": "value is not a valid list",
        },
    ],
)
def test_422_json_model(json_model_kserve_service, data):
    client = TestClient(json_model_kserve_service)
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json"),
        json=data["input"],
    )
    assert response.status_code == 422
    assert data["message"] in str(response.json()["detail"])


@pytest.mark.parametrize("inference_data", json_inference_data)
def test_400_json_model_with_path_not_load(
    json_model_with_path_kserve_service,
    inference_data,
):
    client = TestClient(json_model_with_path_kserve_service)
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json"),
        json=inference_data["request"],
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Model is not loaded. Load the model first."
    )


@pytest.mark.parametrize("inference_data", json_inference_data)
def test_200_json_model_with_path(
    json_model_with_path_kserve_service,
    inference_data,
):
    client = TestClient(json_model_with_path_kserve_service)
    # prediction failed
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json"),
        json=inference_data["request"],
    )
    assert response.status_code == 400
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
    # prediction succeeds
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json"),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert (
        response.json()["outputs"][0]["data"]
        == inference_data["response"]["outputs"][0]["data"]
    )
