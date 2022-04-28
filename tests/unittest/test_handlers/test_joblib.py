import os
import pathlib
import sys

import joblib
import pytest

from pinferencia.handlers import JoblibHandler
from tests.models.sum_product_model import SumProductModel


def test_load():
    # define model path
    model_path = os.path.join(
        pathlib.Path(__file__).parent.resolve(), "sum_product.joblib"
    )
    # dump model
    model = SumProductModel()
    joblib.dump(model, filename=model_path)
    del model
    # load model
    handler = JoblibHandler(model_path=model_path, entrypoint="predict")
    model = handler.load_model()
    # remove pickle file
    os.remove(model_path)
    # predict
    assert model.predict([1, 2, 3, 4]) == {"sum": 10, "product": 24}


def test_load_error():
    model = SumProductModel()
    handler = JoblibHandler(model=model)
    with pytest.raises(Exception) as exc:
        handler.load_model()
    assert "Model path not provided." == str(exc.value)


def test_predict_error():
    handler = JoblibHandler(model_path="abc")
    with pytest.raises(Exception) as exc:
        handler.predict([1, 2])
    assert "Model is not loaded." == str(exc.value)


def test_import_error(monkeypatch):
    handler = JoblibHandler(model_path="abc.joblib")
    monkeypatch.setitem(sys.modules, "joblib", None)
    with pytest.raises(Exception) as exc:
        handler.load_model()
    assert "joblib not installed. To install, run: pip install joblib" == str(exc.value)
