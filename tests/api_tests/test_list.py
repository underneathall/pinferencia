import requests


def test(backend_port):
    response = requests.get(f"http://127.0.0.1:{backend_port}/v1/models")
    models = response.json()
    assert len(models) == 1
    assert len(models[0]["versions"]) == 2
