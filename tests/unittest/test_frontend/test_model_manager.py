from unittest.mock import MagicMock, Mock

import pytest
import requests

from pinferencia.frontend.api_manager.default import APIManager
from pinferencia.frontend.model_manager import ModelManager


def test_init():
    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    assert isinstance(manager.api_manager, APIManager)


def test_init_invalid_api_set():
    with pytest.raises(ImportError) as exc:
        ModelManager(backend_server="http://127.0.0.1:8000", api_set="invalid")
    assert "No module named 'pinferencia.frontend.api_manager.invalid'" == str(
        exc.value
    )


def test_predict(monkeypatch):
    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    mock_api_manager_predict = Mock(return_value="def")
    monkeypatch.setattr(manager.api_manager, "predict", mock_api_manager_predict)

    # without version name
    assert manager.predict(model_name="test", data="abc") == "def"
    assert mock_api_manager_predict.call_count == 1
    assert mock_api_manager_predict.call_args[1]["model_name"] == "test"
    assert mock_api_manager_predict.call_args[1]["data"] == "abc"
    assert mock_api_manager_predict.call_args[1]["version_name"] is None

    # with version name
    assert manager.predict(model_name="test", data="abc", version_name="v1") == "def"
    assert mock_api_manager_predict.call_count == 2
    assert mock_api_manager_predict.call_args[1]["model_name"] == "test"
    assert mock_api_manager_predict.call_args[1]["data"] == "abc"
    assert mock_api_manager_predict.call_args[1]["version_name"] == "v1"


@pytest.mark.parametrize("debug", [True, False])
def test_predict_with_requests_mock_200(debug, monkeypatch):
    # mock requests.post
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.json = Mock(return_value={"data": "def"})
    post_mock = Mock(return_value=response_mock)
    monkeypatch.setattr(requests, "post", post_mock)

    # call predict
    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    manager.api_manager.debug = debug
    assert manager.predict(model_name="test", data="abc") == "def"


@pytest.mark.parametrize("debug", [True, False])
@pytest.mark.parametrize("status_code", [400, 403, 404, 422, 500, 503])
def test_predict_with_requests_mock_non_200(debug, status_code, monkeypatch):
    # mock requests.post
    response_mock = MagicMock()
    response_mock.status_code = status_code
    response_mock.json = Mock(return_value={"data": "def"})
    post_mock = Mock(return_value=response_mock)
    monkeypatch.setattr(requests, "post", post_mock)

    # call predict
    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    manager.api_manager.debug = debug
    assert "Non 200 response from backend" in manager.predict(
        model_name="test", data="abc"
    )


def test_list_model(clear_st_cache, monkeypatch):
    # mock api manager list
    mock_api_manager_list = Mock(return_value=["def"])

    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    monkeypatch.setattr(manager.api_manager, "list", mock_api_manager_list)

    # without model name
    assert manager.list() == ["def"]
    assert mock_api_manager_list.call_count == 1
    assert mock_api_manager_list.call_args[1]["model_name"] is None

    # with model name
    assert manager.list(model_name="test") == ["def"]
    assert mock_api_manager_list.call_count == 2
    assert mock_api_manager_list.call_args[1]["model_name"] == "test"


def test_list_model_exception_non_list(clear_st_cache, monkeypatch):
    # mock api manager list
    mock_api_manager_list = Mock(return_value="def")

    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    monkeypatch.setattr(manager.api_manager, "list", mock_api_manager_list)

    # invalid non list response
    with pytest.raises(Exception) as exc:
        manager.list()
    assert "def" == str(exc.value)


def test_list_model_with_requests_mock(clear_st_cache, monkeypatch):
    # mock requests.get
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.json = Mock(return_value=["def"])
    list_mock = Mock(return_value=response_mock)
    monkeypatch.setattr(requests, "get", list_mock)

    # call list
    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    assert manager.list() == ["def"]


@pytest.mark.parametrize("status_code", [400, 403, 404, 422, 500, 503])
def test_list_model_with_requests_mock_non_200(
    status_code,
    clear_st_cache,
    monkeypatch,
):
    # mock requests.get
    response_mock = MagicMock()
    response_mock.status_code = status_code
    response_mock.json = Mock(return_value=["defghi"])
    list_mock = Mock(return_value=response_mock)
    monkeypatch.setattr(requests, "get", list_mock)

    # call list
    manager = ModelManager(backend_server="http://127.0.0.1:8000")
    with pytest.raises(Exception) as exc:
        result = manager.list()
        print(result)
    assert "Non 200 response from backend" in str(exc.value)
