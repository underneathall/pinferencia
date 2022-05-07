import sys
from unittest.mock import MagicMock

from pinferencia.main import check_dependencies


def test_all_installed(monkeypatch):
    # mock uvicorn and streamlit
    module_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "streamlit", module_mock)
    monkeypatch.setitem(sys.modules, "uvicorn", module_mock)

    # mock sys.exit
    exit_mock = MagicMock()
    monkeypatch.setattr(sys, "exit", exit_mock)

    check_dependencies()
    assert not exit_mock.called


def test_no_streamlit(monkeypatch):
    # mock missing streamlit module
    monkeypatch.setitem(sys.modules, "streamlit", None)

    # mock sys.exit
    exit_mock = MagicMock()
    monkeypatch.setattr(sys, "exit", exit_mock)

    check_dependencies()
    assert exit_mock.called
    assert exit_mock.call_args[0][0] == (
        "You need to install streamlit to start the frontend. "
        "To install streamlit, run: pip install streamlit"
    )


def test_no_uvicorn(monkeypatch):
    # mock missing uvicorn module
    st_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "streamlit", st_mock)
    monkeypatch.setitem(sys.modules, "uvicorn", None)

    # mock sys.exit
    exit_mock = MagicMock()
    monkeypatch.setattr(sys, "exit", exit_mock)

    check_dependencies()
    assert exit_mock.called
    assert exit_mock.call_args[0][0] == (
        "You need to install uvicorn to start the backend. "
        "To install uvicorn, run: pip install uvicorn"
    )
