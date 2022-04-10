import copy

import pytest
from fastapi.testclient import TestClient

from .data import json_inference_data, sum_prod_inference_data

BASE_URL = "/v1/models/{model_name}/versions/{version_name}"
TEST_PREDICT_URL = BASE_URL + "/infer"
TEST_READY_URL = BASE_URL + "/ready"
TEST_LOAD_URL = BASE_URL + "/load"


@pytest.mark.parametrize("inference_data", json_inference_data)
@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_predict_json_model_versions_200(
    json_model_kserve_service,
    inference_data,
    version_name,
):
    client = TestClient(json_model_kserve_service)
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json", version_name=version_name),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert (
        response.json()["predictions"]
        == inference_data["response"]["predictions"]
    )


@pytest.mark.parametrize("inference_data", sum_prod_inference_data)
@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_predict_sum_product_versions_200(
    sum_product_model_kserve_service,
    inference_data,
    version_name,
):
    client = TestClient(sum_product_model_kserve_service)
    response = client.post(
        TEST_PREDICT_URL.format(
            model_name="sum_prod", version_name=version_name
        ),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    print("response.json()", response.json())
    print("inference_data", inference_data)
    test_inference_data = copy.deepcopy(inference_data)
    for k, v in response.json()["predictions"].items():
        assert v == test_inference_data["response"]["predictions"].pop(k)
    assert not test_inference_data["response"]["predictions"]


@pytest.mark.parametrize("version_name", ["default", "v1"])
@pytest.mark.parametrize("inference_data", json_inference_data)
def test_400_json_model_with_path_not_load(
    json_model_with_path_kserve_service,
    version_name,
    inference_data,
):
    client = TestClient(json_model_with_path_kserve_service)
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json", version_name=version_name),
        json=inference_data["request"],
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Model is not loaded. Load the model first."
    )


@pytest.mark.parametrize("version_name", ["default", "v1"])
@pytest.mark.parametrize("inference_data", json_inference_data)
def test_200_json_model_with_path(
    json_model_with_path_kserve_service,
    version_name,
    inference_data,
):
    client = TestClient(json_model_with_path_kserve_service)
    # prediction failed
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json", version_name=version_name),
        json=inference_data["request"],
    )
    assert response.status_code == 400
    # model is not ready
    response = client.get(
        TEST_READY_URL.format(model_name="json", version_name=version_name)
    )
    assert response.status_code == 200
    assert not response.json()
    # load the model
    response = client.post(
        TEST_LOAD_URL.format(model_name="json", version_name=version_name)
    )
    assert response.status_code == 200
    assert response.json()
    # model is ready
    response = client.get(
        TEST_READY_URL.format(model_name="json", version_name=version_name)
    )
    assert response.status_code == 200
    assert response.json()
    # prediction succeeds
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json", version_name=version_name),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert (
        response.json()["predictions"]
        == inference_data["response"]["predictions"]
    )


@pytest.mark.parametrize("version_name", ["loaded"])
@pytest.mark.parametrize("inference_data", json_inference_data)
def test_200_json_model_with_path_loaded(
    json_model_with_path_kserve_service,
    version_name,
    inference_data,
):
    client = TestClient(json_model_with_path_kserve_service)
    # model is ready
    response = client.get(
        TEST_READY_URL.format(model_name="json", version_name=version_name)
    )
    assert response.status_code == 200
    assert response.json()
    # prediction succeeds
    response = client.post(
        TEST_PREDICT_URL.format(model_name="json", version_name=version_name),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert (
        response.json()["predictions"]
        == inference_data["response"]["predictions"]
    )
