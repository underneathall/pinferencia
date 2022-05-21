from fastapi.testclient import TestClient

TEST_URL = "/v2/models/{model_name}"


def test_get_json_model_versions(json_model_kserve_service):
    client = TestClient(json_model_kserve_service)
    response = client.get(TEST_URL.format(model_name="json"))
    assert response.status_code == 200
    assert response.json() == [
        {
            "inputs": [],
            "name": "default",
            "outputs": [],
            "platform": "",
            "task": "",
            "display_name": "",
            "description": "",
            "input_type": "",
            "output_type": "",
        },
        {
            "inputs": [],
            "name": "v1",
            "outputs": [],
            "platform": "",
            "task": "",
            "display_name": "",
            "description": "",
            "input_type": "",
            "output_type": "",
        },
    ]
