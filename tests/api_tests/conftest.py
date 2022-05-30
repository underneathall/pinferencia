import shlex
import time
from subprocess import Popen

import pytest
import requests


@pytest.fixture(scope="session")
def backend_port():
    return 9999


@pytest.fixture(autouse=True, scope="session")
def backend(backend_port):
    args = shlex.split(
        f"uvicorn --port {backend_port} tests.api_tests.app:service"
    )
    p = Popen(args)
    for _ in range(60):
        try:
            requests.get(f"http://127.0.0.1:{backend_port}")
        except Exception:
            time.sleep(1)
    yield
    p.kill()
