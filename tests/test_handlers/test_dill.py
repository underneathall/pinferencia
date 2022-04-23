import os
import pathlib
import sys

import dill
import pytest

from pinferencia.handlers import DillHandler
from tests.models.sum_product_model import SumProductModel


def test_load_dill():
    # define model path
    model_path = os.path.join(
        pathlib.Path(__file__).parent.resolve(), "sum_product.pkl"
    )
    # dump model
    model = SumProductModel()
    with open(model_path, "wb") as f:
        dill.dump(model, file=f)
    del model
    # load model
    handler = DillHandler(model_path=model_path, entrypoint="predict")
    model = handler.load_model()
    # remove pickle file
    os.remove(model_path)
    # predict
    assert model.predict([1, 2, 3, 4]) == {"sum": 10, "product": 24}


def test_load_error():
    model = SumProductModel()
    handler = DillHandler(model=model)
    with pytest.raises(Exception) as exc:
        handler.load_model()
    assert "Model path not provided." == str(exc.value)


def test_predict_error():
    handler = DillHandler(model_path="abc")
    with pytest.raises(Exception) as exc:
        handler.predict([1, 2])
    assert "Model is not loaded." == str(exc.value)


def test_import_error(monkeypatch):
    handler = DillHandler(model_path="abc.pkl")
    monkeypatch.setitem(sys.modules, "dill", None)
    with pytest.raises(Exception) as exc:
        handler.load_model()
    assert "dill not installed. To install, run: pip install dill" == str(
        exc.value
    )
