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
                },
                {
                    "name": "v1",
                    "platform": "",
                    "device": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                },
            ],
        },
    ]


def test_list_dummy_model(dummy_model_service):
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
                },
                {
                    "name": "v1",
                    "platform": "",
                    "device": "",
                    "task": task.TEXT_TO_TEXT,
                    "display_name": "Dummy Model V1",
                    "description": "This is a dummy model v1.",
                },
            ],
        },
    ]
