import pytest
from fastapi.testclient import TestClient

from pinferencia import task

TEST_URL = "/v1/models"


def test_list_json_models(json_model_default_service):
    client = TestClient(json_model_default_service)
    response = client.get(TEST_URL)
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "json",
            "versions": [
                {
                    "name": "default",
                    "platform": "",
                    "device": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                    "input_type": "",
                    "output_type": "",
                },
                {
                    "name": "v1",
                    "platform": "",
                    "device": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                    "input_type": "",
                    "output_type": "",
                },
            ],
        },
    ]


def test_list_json_model_with_path(json_model_with_path_default_service):
    client = TestClient(json_model_with_path_default_service)
    response = client.get(TEST_URL)
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "json",
            "versions": [
                {
                    "name": "default",
                    "platform": "",
                    "device": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                    "input_type": "",
                    "output_type": "",
                },
                {
                    "name": "v1",
                    "platform": "",
                    "device": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                    "input_type": "",
                    "output_type": "",
                },
                {
                    "name": "loaded",
                    "platform": "",
                    "device": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                    "input_type": "",
                    "output_type": "",
                },
            ],
        },
    ]


@pytest.mark.parametrize("use_decorator", [True, False])
def test_list_dummy_model(
    use_decorator, dummy_model_service, dummy_model_service_with_decorator
):
    if use_decorator:
        client = TestClient(dummy_model_service_with_decorator)
    else:
        client = TestClient(dummy_model_service)
    response = client.get(TEST_URL)
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "dummy",
            "versions": [
                {
                    "name": "default",
                    "task": task.TEXT_TO_TEXT,
                    "display_name": "Dummy Model",
                    "description": "This is a dummy model.",
                    "device": "CPU",
                    "platform": "linux",
                    "input_type": "str",
                    "output_type": "str",
                },
                {
                    "name": "v1",
                    "platform": "",
                    "device": "",
                    "task": task.TEXT_TO_TEXT,
                    "display_name": "Dummy Model V1",
                    "description": "This is a dummy model v1.",
                    "input_type": "list",
                    "output_type": "list",
                },
            ],
        },
    ]
