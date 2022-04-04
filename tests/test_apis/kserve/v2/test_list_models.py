from fastapi.testclient import TestClient

TEST_URL = "/v2/models"


def test_list_json_models(json_model_kserve_service):
    client = TestClient(json_model_kserve_service)
    response = client.get(TEST_URL)
    assert response.status_code == 200
    assert response.json() == [
        {
            "inputs": [],
            "name": "json",
            "outputs": [],
            "platform": "",
            "versions": [
                {
                    "inputs": [],
                    "name": "default",
                    "outputs": [],
                    "platform": "",
                },
                {"inputs": [], "name": "v1", "outputs": [], "platform": ""},
            ],
        },
    ]
