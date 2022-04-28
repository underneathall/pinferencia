from fastapi.testclient import TestClient

TEST_URL = "/v1/models"


def test_list_json_models(json_model_kserve_service):
    client = TestClient(json_model_kserve_service)
    response = client.get(TEST_URL)
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "json",
            "platform": "",
            "versions": [
                {
                    "name": "default",
                    "platform": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                },
                {
                    "name": "v1",
                    "platform": "",
                    "task": "",
                    "display_name": "",
                    "description": "",
                },
            ],
        },
    ]
