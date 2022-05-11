import sys
from unittest.mock import MagicMock, Mock

import pytest

from pinferencia.main import check_port_availability, socket


@pytest.mark.parametrize("backend_bind", [Exception("Not available"), True])
@pytest.mark.parametrize("frontend_bind", [Exception("Not available"), True])
@pytest.mark.parametrize("mode", ["all", "frontend", "backend"])
def test(backend_bind, frontend_bind, mode, monkeypatch):
    # mock sys.exit
    exit_mock = MagicMock()
    monkeypatch.setattr(sys, "exit", exit_mock)

    # mock socket.bind
    side_effect = []
    if mode != "frontend":
        side_effect.append(backend_bind)
    if mode != "backend":
        side_effect.append(frontend_bind)
    bind_mock = Mock(side_effect=side_effect)
    socket_mock = MagicMock()
    socket_mock.bind = bind_mock
    monkeypatch.setattr(socket, "socket", Mock(return_value=socket_mock))

    check_port_availability(
        backend_host="127.0.0.1",
        backend_port="8000",
        frontend_host="127.0.0.1",
        frontend_port="8051",
        mode=mode,
    )
    expect_called = False
    expected_msg = ""
    if backend_bind is not True and mode != "frontend":
        expect_called = True
        expected_msg += "Port 8000 is in use. Try another port with --backend-port.\n"
    if frontend_bind is not True and mode != "backend":
        expect_called = True
        expected_msg += "Port 8051 is in use. Try another port with --frontend-port.\n"

    if expect_called:
        assert exit_mock.called
        assert exit_mock.call_args[0][0] == expected_msg


def test_duplicat_port():
    with pytest.raises(Exception) as exc:
        check_port_availability(
            backend_host="127.0.0.1",
            backend_port="8000",
            frontend_host="127.0.0.1",
            frontend_port="8000",
        )
    assert str(exc.value) == "Choose different ports for backend and frontend."
