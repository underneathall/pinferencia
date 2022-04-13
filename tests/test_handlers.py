import os
import pathlib
import pickle
import random
from unittest.mock import patch

import pytest

from pinferencia.context import PredictContext
from pinferencia.handlers import BaseHandler, PickleHandler
from tests.models.sum_product_model import SumProductModel


def test_incorrect_extend():
    class TestHandler(BaseHandler):
        pass

    with pytest.raises(TypeError) as exc:
        TestHandler(model_path="abc")
    assert (
        "Can't instantiate abstract class TestHandler" " with abstract method"
    ) in str(exc.value)
    assert "load_model" in str(exc.value)


def test_instantiate():
    with pytest.raises(TypeError) as exc:
        BaseHandler(model_path="abc")
    assert (
        "Can't instantiate abstract class BaseHandler" " with abstract method"
    ) in str(exc.value)
    assert "load_model" in str(exc.value)


@patch.multiple(BaseHandler, __abstractmethods__=set())
def test_base_class_predict():
    def predict(data):
        return sum(data)

    assert (
        BaseHandler(model_path="abc", model=predict).predict([1, 2, 3, 4])
        == 10
    )


@patch.multiple(BaseHandler, __abstractmethods__=set())
def test_abstract_load_model():
    assert BaseHandler(model_path="abc").load_model() == NotImplemented


def test_incorrect_instantiate():
    with pytest.raises(Exception) as exc:
        PickleHandler()
    assert "At least one of model or model path must be provided." == str(
        exc.value
    )


def test_set_context():
    scheme = "abc"
    request_data = [1, 2]
    handler = PickleHandler("abc")
    handler.set_context(
        PredictContext(scheme=scheme, request_data=request_data)
    )
    assert handler.context.scheme == scheme
    assert handler.context.request_data == request_data


def test_process():
    class TestHandler(BaseHandler):
        def preprocess(self, data: object, parameters: object = None):
            return data + 1

        def postprocess(self, data: object, parameters: object = None):
            return data + 2

        def predict(self, data: object):
            return data + 4

        def load_model(self):
            return None

    handler = TestHandler("abc")
    data = random.randint(-1000, 1000)
    assert handler.preprocess(data) == data + 1
    assert handler.postprocess(data) == data + 2
    assert handler.predict(data) == data + 4
    assert handler.process(data) == data + 7


def test_load_pickle():
    # define model path
    model_path = os.path.join(
        pathlib.Path(__file__).parent.resolve(), "sum_product.pkl"
    )
    # dump model
    model = SumProductModel()
    with open(model_path, "wb") as f:
        pickle.dump(model, file=f)
    del model
    # load model
    handler = PickleHandler(model_path=model_path, entrypoint="predict")
    model = handler.load_model()
    # remove pickle file
    os.remove(model_path)
    # predict
    assert model.predict([1, 2, 3, 4]) == {"sum": 10, "product": 24}


def test_load_error():
    model = SumProductModel()
    handler = PickleHandler(model=model)
    with pytest.raises(Exception) as exc:
        handler.load_model()
    assert "Model path not provided." == str(exc.value)


def test_predict_error():
    handler = PickleHandler(model_path="abc")
    with pytest.raises(Exception) as exc:
        handler.predict([1, 2])
    assert "Model is not loaded." == str(exc.value)
