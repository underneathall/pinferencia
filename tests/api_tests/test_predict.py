import requests


def test(backend_port):
    response = requests.post(
        f"http://127.0.0.1:{backend_port}/v1/models/test/predict",
        json={"data": "abc"},
    )
    prediction = response.json()
    assert prediction["data"] == "abc"
