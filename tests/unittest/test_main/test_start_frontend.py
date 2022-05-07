import sys
from unittest.mock import MagicMock

from pinferencia.main import start_frontend


def test_with_file_content(monkeypatch):
    # mock the bootstrap module
    bootstrap_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "streamlit.bootstrap", bootstrap_mock)

    # start frontend
    start_frontend("abc", a=1, b=2)

    # assert bootstrap.run is correctly called
    assert bootstrap_mock.run.call_count == 1
    assert "proxy.py" in bootstrap_mock.run.call_args[0][0]
    assert bootstrap_mock.run.call_args[1]["flag_options"]["a"] == 1
    assert bootstrap_mock.run.call_args[1]["flag_options"]["b"] == 2


def test_with_main_script_path(monkeypatch):
    # mock the bootstrap module
    bootstrap_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "streamlit.bootstrap", bootstrap_mock)

    # start frontend
    start_frontend("abc", main_script_path="abc.py", a=1, b=2)

    # assert bootstrap.run is correctly called
    assert bootstrap_mock.run.call_count == 1
    assert bootstrap_mock.run.call_args[0][0] == "abc.py"
    assert bootstrap_mock.run.call_args[1]["flag_options"]["a"] == 1
    assert bootstrap_mock.run.call_args[1]["flag_options"]["b"] == 2
