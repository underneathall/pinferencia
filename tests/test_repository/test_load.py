from unittest.mock import Mock

from pinferencia.handlers import BaseHandler
from pinferencia.repository import ModelRepository


def test_load_model():
    mock_load = Mock(return_value=True)

    class TestHandler(BaseHandler):
        def load_model(self):
            return mock_load()

        def predict(self, data):
            return data

    repository = ModelRepository()
    assert repository.register(
        model_name="test",
        model="abc",
        handler=TestHandler,
        load_now=False,
    )
    assert mock_load.call_count == 0
    assert repository.load_model(model_name="test")
    assert mock_load.call_count == 1


def test_load_model_load_now():
    mock_load = Mock(return_value=True)

    class TestHandler(BaseHandler):
        def load_model(self):
            return mock_load()

        def predict(self, data):
            return data

    repository = ModelRepository()
    assert repository.register(
        model_name="test",
        model="abc",
        handler=TestHandler,
    )
    assert mock_load.call_count == 1


def test_load_model_error():
    class TestHandler(BaseHandler):
        def load_model(self):
            raise Exception("Load Error")

        def predict(self, data):
            return data

    repository = ModelRepository()
    assert not repository.register(
        model_name="test", model="abc", handler=TestHandler
    )
    assert not repository.load_model(model_name="test")
