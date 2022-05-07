import ssl
import sys
from unittest.mock import MagicMock, Mock

import pytest
from click.testing import CliRunner
from uvicorn.config import LOGGING_CONFIG, SSL_PROTOCOL_VERSION

from pinferencia.main import main

BACKEND_DEFAULT_VALUE = {
    "mode": "all",
    "host": "127.0.0.1",
    "port": 8000,
    "debug": False,
    "workers": None,
    "env_file": None,
    "log_config": LOGGING_CONFIG,
    "log_level": None,
    "root_path": "",
    "limit_concurrency": None,
    "backlog": 2048,
    "limit_max_requests": None,
    "timeout_keep_alive": 5,
    "ssl_keyfile": None,
    "ssl_certfile": None,
    "ssl_keyfile_password": None,
    "ssl_version": int(SSL_PROTOCOL_VERSION),
    "ssl_cert_reqs": int(ssl.CERT_NONE),
    "ssl_ca_certs": None,
    "ssl_ciphers": "TLSv1",
    "app_dir": ".",
    "reload": False,
}

FRONTEND_DEFAULT_VALUE = {
    "frontend_base_url_path": "",
    "frontend_port": 8501,
    "frontend_host": "127.0.0.1",
    "frontend_browser_server_address": "localhost",
}


@pytest.mark.parametrize(
    "backend_arg",
    [
        ["--backend-host", "127.0.0.1"],
        ["--backend-port", 8000],
        ["--backend-debug"],
        ["--backend-workers", 2],
        ["--backend-env-file", "/"],
        ["--backend-log-config", "/"],
        ["--backend-log-level", "error"],
        ["--backend-root-path", "/a/b/c"],
        ["--backend-limit-concurrency", 100],
        ["--backend-backlog", 4096],
        ["--backend-limit-max-requests", 111],
        ["--backend-timeout-keep-alive", 15],
        ["--ssl-keyfile", "abc"],
        ["--ssl-certfile", "abc"],
        ["--ssl-keyfile-password", "abc"],
        ["--ssl-version", 1],
        ["--ssl-cert-reqs", 1],
        ["--ssl-ca-certs", "abc"],
        ["--ssl-ciphers", "TLSv2"],
        ["--backend-app-dir", "/a/b/c"],
        ["--reload"],
    ],
)
@pytest.mark.parametrize(
    "frontend_arg",
    [
        ["--frontend-base-url-path", ""],
        ["--frontend-port", 8501],
        ["--frontend-host", "127.0.0.1"],
        ["--frontend-browser-server-address", "localhost"],
        ["--frontend-script", "abc.py"],
    ],
)
@pytest.mark.parametrize(
    "mode",
    ["all", "backend", "frontend", "", "invalid"],
)
def test_args(backend_arg, frontend_arg, mode, monkeypatch):
    if len(backend_arg) > 1:
        backend_arg_name, backend_arg_value = backend_arg
    else:
        backend_arg_name, backend_arg_value = backend_arg[0], True
    frontend_arg_name, frontend_arg_value = frontend_arg

    mode_arg = []
    if mode:
        mode_arg += ["--mode", mode]

    monkeypatch.setattr(
        "pinferencia.main.check_port_availability",
        Mock(return_value=True),
    )
    monkeypatch.setattr(
        "pinferencia.main.check_dependencies",
        Mock(return_value=True),
    )

    # mock uvicorn.run
    uvicorn_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "uvicorn", uvicorn_mock)

    # mock the bootstrap module
    bootstrap_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "streamlit.bootstrap", bootstrap_mock)

    process_start_monitor = MagicMock()

    class FakeProcess:
        def __init__(self, target, args, kwargs):
            uvicorn_mock.run()
            self.target = target
            self.args = args
            self.kwargs = kwargs

        def start(self):
            process_start_monitor()
            return self.target(*self.args, **self.kwargs)

    monkeypatch.setattr("pinferencia.main.Process", FakeProcess)

    runner = CliRunner()
    result = runner.invoke(
        main, ["app:service", *mode_arg, *backend_arg, *frontend_arg]
    )
    if mode != "invalid":
        assert result.exit_code == 0
    else:
        assert result.exit_code >= 0
    if not mode or mode == "all":
        assert process_start_monitor.called

    if mode in ["all", "backend"]:
        # convert cli argument name to python argument name
        parsed_backend_arg_name = (
            backend_arg_name.replace("--", "").replace("backend-", "").replace("-", "_")
        )
        assert uvicorn_mock.run.called
        assert (
            uvicorn_mock.run.call_args[1][parsed_backend_arg_name] == backend_arg_value
        )
        backend_call_kwargs = uvicorn_mock.run.call_args[1]
        for k in backend_call_kwargs:
            if k == parsed_backend_arg_name:
                assert backend_call_kwargs[k] == backend_arg_value
            else:
                assert backend_call_kwargs[k] == BACKEND_DEFAULT_VALUE[k]

    if mode in ["all", "frontend"]:
        # convert cli argument name to python argument name
        parsed_frontend_arg_name = (
            frontend_arg_name.replace("--", "")
            .replace("frontend-", "")
            .replace("-", "_")
        )
        assert bootstrap_mock.run.called
        frontend_call_kwargs = bootstrap_mock.run.call_args[1]["flag_options"]

        if frontend_arg[0] == "--frontend-script":
            assert bootstrap_mock.run.call_args[0][0] == frontend_arg_value
        frontend_kwargs_key_map = {
            "server.baseUrlPath": "frontend_base_url_path",
            "server.port": "frontend_port",
            "server.address": "frontend_host",
            "browser.serverAddress": "frontend_browser_server_address",
        }
        for k in frontend_call_kwargs:
            if frontend_kwargs_key_map[k] == parsed_frontend_arg_name:
                assert frontend_call_kwargs[k] == frontend_arg_value
            else:
                assert (
                    frontend_call_kwargs[k]
                    == FRONTEND_DEFAULT_VALUE[frontend_kwargs_key_map[k]]
                )


def test_https(monkeypatch):
    monkeypatch.setattr(
        "pinferencia.main.check_port_availability",
        Mock(return_value=True),
    )
    monkeypatch.setattr(
        "pinferencia.main.check_dependencies",
        Mock(return_value=True),
    )

    # mock uvicorn.run
    uvicorn_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "uvicorn", uvicorn_mock)

    # mock the bootstrap module
    bootstrap_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "streamlit.bootstrap", bootstrap_mock)

    process_start_monitor = MagicMock()

    class FakeProcess:
        def __init__(self, target, args, kwargs):
            uvicorn_mock.run()
            self.target = target
            self.args = args
            self.kwargs = kwargs

        def start(self):
            process_start_monitor()
            return self.target(*self.args, **self.kwargs)

    mock_start_frontend = MagicMock()
    monkeypatch.setattr("pinferencia.main.Process", FakeProcess)
    monkeypatch.setattr("pinferencia.main.start_frontend", mock_start_frontend)

    runner = CliRunner()
    result = runner.invoke(
        main, ["app:service", "--ssl-keyfile", "abc", "--ssl-certfile", "abc"]
    )
    assert result.exit_code == 0
    assert process_start_monitor.called

    assert mock_start_frontend.called
    assert "https" in mock_start_frontend.call_args[0][0]
