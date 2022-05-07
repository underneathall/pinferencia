import sys
from unittest.mock import MagicMock

from pinferencia.main import start_backend


def test(monkeypatch):
    # mock uvicorn.run
    uvicorn_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "uvicorn", uvicorn_mock)

    # start backend
    start_backend("abc", a=1, b=2)

    # assert bootstrap.run is correctly called
    assert uvicorn_mock.run.call_count == 1
    assert uvicorn_mock.run.call_args[0][0] == "abc"
    assert uvicorn_mock.run.call_args[1]["a"] == 1
    assert uvicorn_mock.run.call_args[1]["b"] == 2
