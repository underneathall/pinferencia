import pytest


@pytest.fixture(scope="session")
def json_model_data():
    return [
        {"request_data": "a", "response_data": 1},
        {"request_data": "b", "response_data": 2},
        {"request_data": "c", "response_data": 3},
        {"request_data": "d", "response_data": 0},
    ]


@pytest.fixture(scope="session")
def json_model():
    from .models.json_model.model import model

    return model


@pytest.fixture(scope="session")
def json_model_path():
    from .models.json_model.model import model_path

    return model_path


@pytest.fixture(scope="session")
def json_model_dir():
    from .models.json_model.model import model_dir

    return model_dir


@pytest.fixture(scope="session")
def json_model_handler():
    from .models.json_model.handler import JsonHandler

    return JsonHandler


@pytest.fixture(scope="session")
def sum_product_model():
    from .models.sum_product_model import model

    return model


@pytest.fixture
def sum_product_model_metadata():
    from .models.sum_product_model import metadata

    return metadata
