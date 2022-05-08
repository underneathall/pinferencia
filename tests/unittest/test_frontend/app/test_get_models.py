from unittest.mock import MagicMock, Mock

import requests

from pinferencia.frontend.app import Server, st, time


def test_connection_error(monkeypatch):
    # mock time.sleep
    mock_sleep = MagicMock()
    monkeypatch.setattr(time, "sleep", mock_sleep)

    # mock st.empty() to return a MagicMock instance
    mock_empty_container = MagicMock()
    monkeypatch.setattr(st, "empty", Mock(return_value=mock_empty_container))

    # mock st.warning
    mock_warning = MagicMock()
    monkeypatch.setattr(st, "warning", mock_warning)

    # mock requests.get
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.json = Mock(side_effect=Exception("Connection Error."))
    post_mock = Mock(return_value=response_mock)
    monkeypatch.setattr(requests, "get", post_mock)

    Server(backend_server="http://127.0.0.1:8111")

    # assert time.sleep is called 10 times
    assert mock_sleep.call_count == 9

    # assert the reconnect info is correctly called
    assert mock_empty_container.info.call_count == 10
    for args in mock_empty_container.call_args_list:
        assert "Backend is starting. Retry in 5s: attempt" in args[0][0]

    # assert after 10 failure connections, a warning is correctly displayed
    assert mock_warning.call_count == 1
    assert (
        "Please check if the backend is running, and refresh the page manually."
        == mock_warning.call_args[0][0]
    )
