from unittest.mock import MagicMock, patch

import pytest

from pinferencia.frontend.api_manager.base import BaseManager


def test_abstractmethod():
    class TestManager(BaseManager):
        pass

    with pytest.raises(TypeError) as exc:
        TestManager()
    assert (
        "Can't instantiate abstract class TestManager with abstract "
        "methods parse_response_data, prepare_request_data"
    ) == str(exc.value)


@patch.multiple(BaseManager, __abstractmethods__=set())
def test_abstract_parse_response_data():
    assert (
        BaseManager(server="http://127.0.0.1:8000").parse_response_data({"data": 1})
        == NotImplemented
    )


@patch.multiple(BaseManager, __abstractmethods__=set())
def test_abstract_prepare_request_data():
    assert (
        BaseManager(server="http://127.0.0.1:8000").prepare_request_data({"data": 1})
        == NotImplemented
    )


@patch.multiple(BaseManager, __abstractmethods__=set())
def test_abstract_display_debug_json_data():
    component = MagicMock()
    BaseManager(server="http://127.0.0.1:8000").display_debug_json_data(
        {"data": "abc"},
        component=component,
    )
    assert component.json.called
    assert component.json.call_args[0][0] == {"data": "abc"}


@patch.multiple(BaseManager, __abstractmethods__=set())
def test_abstract_display_debug_json_data_large_data():
    component = MagicMock()
    data = {"data": "abc" * 200}
    BaseManager(server="http://127.0.0.1:8000").display_debug_json_data(
        data,
        component=component,
    )
    assert component.warning.called
    assert component.code.called
    assert component.code.call_args[1]["body"] == str(data)[:500] + "..."
    assert component.code.call_args[1]["language"] == "text"
