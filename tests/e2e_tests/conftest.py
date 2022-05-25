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
    return "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+uhfwXqy2Ph25VYnPiB3SzhUkPlXCfNkAAEsCCCeOeKx9RsLjStUu9Ou1C3NpM8Eqg5AdSVIz35FVqK9xl0HXhb/C20sdMubjTLMQXs11AhkRXmmDsCwzgAYPpz+XI/GrSLrTfiVqNzPapbw3xE8AWQNvUAKXOOmWVjg+teeUV2fgXxd4hsPE2hWEGuX8Vh9uhja3Fw3lbGcBhtzjGCad8XI7iL4p68twHDGcMm45+QqCuPbBFcVRRU97fXepXb3d9dT3VzJjfNPIXdsAAZY8nAAH4VBX/9k="  # noqa


@pytest.fixture
def image_byte(image_base64_string):
    return BytesIO(base64.b64decode(image_base64_string))
