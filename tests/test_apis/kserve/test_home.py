from fastapi.testclient import TestClient


def test_200(json_model_kserve_service):
    client = TestClient(json_model_kserve_service)
    response = client.get("/")
    assert response.status_code == 200
    response.history[0].headers["location"] == "/docs"
    assert response.history[0].status_code == 307
