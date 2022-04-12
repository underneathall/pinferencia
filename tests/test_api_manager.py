from unittest.mock import patch

import pytest

from pinferencia import Server
from pinferencia.api_manager import BaseAPIManager


def test_extend_base_class():
    service = Server()

    class TestAPIManager(BaseAPIManager):
        def register_route(self):
            return None

    assert (
        TestAPIManager(service).validate_model_metadata(
            model_name="any",
            metadata={"a": 1},
        )
        == []
    )
    assert TestAPIManager(service).register_route() is None


def test_incorrect_extend():
    class TestAPIManager(BaseAPIManager):
        pass

    with pytest.raises(TypeError) as exc:
        service = Server()
        TestAPIManager(service)
    assert (
        "Can't instantiate abstract class TestAPIManager"
        " with abstract method"
    ) in str(exc.value)
    assert "register_route" in str(exc.value)


def test_instantiate():
    with pytest.raises(TypeError) as exc:
        service = Server()
        BaseAPIManager(service)
    assert (
        "Can't instantiate abstract class BaseAPIManager"
        " with abstract method"
    ) in str(exc.value)
    assert "register_route" in str(exc.value)


@patch.multiple(BaseAPIManager, __abstractmethods__=set())
def test_abstract_register_route():
    service = Server()
    assert BaseAPIManager(service).register_route() == NotImplemented
