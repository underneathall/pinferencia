import base64
import time
from io import BytesIO
from multiprocessing import Process

import pytest
import requests

from pinferencia.main import file_content, start_backend, start_frontend


@pytest.fixture(scope="session")
def frontend_kwargs():
    return {
        "server.port": 9917,
        "server.address": "127.0.0.1",
    }


@pytest.fixture(scope="session")
def backend_kwargs():
    return {
        "app_dir": ".",
        "host": "127.0.0.1",
        "port": 9910,
    }


@pytest.fixture(scope="session")
def frontend_addr(frontend_kwargs):
    addr = frontend_kwargs["server.address"]
    port = frontend_kwargs["server.port"]
    return f"http://{addr}:{port}"


@pytest.fixture
def page(frontend_addr):
    from playwright.sync_api import sync_playwright

    launch_args = [
        "--use-fake-ui-for-media-stream",
        "--use-fake-device-for-media-stream",
    ]

    with sync_playwright() as p:
        # visit frontend
        browser = p.chromium.launch(args=launch_args)
        page = browser.new_page(permissions=["camera"])
        page.goto(frontend_addr)

        yield page

        browser.close()


@pytest.fixture(autouse=True, scope="session")
def frontend(frontend_addr, frontend_kwargs, backend_kwargs):
    backend_address = f'http://{backend_kwargs["host"]}:{backend_kwargs["port"]}'
    # start frontend
    frontend_proc = Process(
        target=start_frontend,
        args=[file_content.format(backend_address=backend_address)],
        kwargs=frontend_kwargs,
    )
    frontend_proc.start()
    # TODO: poll if the service is available
    # time.sleep(5)
    for i in range(60):
        try:
            requests.get(frontend_addr)
        except Exception:
            time.sleep(1)
    yield

    frontend_proc.terminate()


@pytest.fixture(autouse=True, scope="session")
def backend(backend_kwargs):
    app = "tests.e2e_tests.demo_app:service"
    backend_proc = Process(target=start_backend, args=[app], kwargs=backend_kwargs)
    backend_proc.start()
    yield

    backend_proc.terminate()


@pytest.fixture
def image_base64_string():
    return "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAIAAAD9b0jDAAADEUlEQVR4nK1WzUrrQBQ+M9NJ0qRJCg1WiBu7cKeCSxGRbrp051bQrQu34gv4BvoEPkhfoNCFKELBhQhaa2z6l99zF+cyNyDW9t77LcJM5uSb78z5mQDMBWMMAKSUmqYBgK7rmqZxzgFAPaWU80n+wDRNGpTLZRqsrKyoVSGEMhBClEqlRXkVHMehgeu6QgjDMIp+GIZBqn+GEAIApJRKhfqSuGgVACqVyt8IBADLsopTwzCU1+p8FgJjLAzDIAiU2N3d3dPTUyJVZrquL8pomqYQYjgc9no9APA8DwAeHx9fXl5s21ZmpVKJMaYO5GdcXFwg4uvrK023t7eHwyEi0pRzrhwvCp8HIUStVkPE2Wy2s7Pjuq7rur1eL03Tk5MTstF13bIsKITu937fkSLi+/v729ubpmm+739+foZhmOc557zVakkpLcuKomg8HsPiCSCEOD4+TpLk/v6eQsEY63Q6cRx/fHwodY7jfK2ob5VmWVav10ul0vX1NdWoaZqu6zLGOOeGYdBOURR9jdK88trf359MJp1OJwzDarUaBAGdwM3NzWw2I2+iKCLVKoDzlFYqlUajYZpmu90GgCAIbNu2bVvTtDRNm82m53m6rlNKFRnnodVqIWK/37+8vDw4ONjY2PA87+7uDhGjKMrz/PDwkCyllEs0qsFgkCRJFEWIiIjdbhcR0zTNsgwR9/b2AKBcLi9RUQBwdHTU7XaJNAxDok7TtN1ub21tkQ3FbYmKAoB6ve77/tra2vr6+vn5+dPTUxzHV1dX1LGURmppP0Pls1Lh+/7DwwMinp2d0Rsqp6/4Nvqj0QgAOOeqxT0/P0+nUwCQUlarVcaYSqxFSQHANE06xDRNydNarZYkCWNsPB4jYpZlS5NOJhNKQCklJfl0OhVCrK6uJkkCAORBHMeLNhTHcVRvVtSj0Yhz3mw26dbL87xosCioAZODhmHc3t7GcYyIm5ubtKUQgnO+6MX3HQaDQb/fV1P1P/BPpADQaDQAwHEc9WPxf1CMOKVdcXXpfXzfh8KlpGmaEIJyS+EXXIc7GO0j1jYAAAAASUVORK5CYII="  # noqa


@pytest.fixture
def image_byte(image_base64_string):
    return BytesIO(base64.b64decode(image_base64_string))
