import pytest
import numpy as np


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


@pytest.fixture
def image_base64_string():
    return "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAIAAAD9b0jDAAADEUlEQVR4nK1WzUrrQBQ+M9NJ0qRJCg1WiBu7cKeCSxGRbrp051bQrQu34gv4BvoEPkhfoNCFKELBhQhaa2z6l99zF+cyNyDW9t77LcJM5uSb78z5mQDMBWMMAKSUmqYBgK7rmqZxzgFAPaWU80n+wDRNGpTLZRqsrKyoVSGEMhBClEqlRXkVHMehgeu6QgjDMIp+GIZBqn+GEAIApJRKhfqSuGgVACqVyt8IBADLsopTwzCU1+p8FgJjLAzDIAiU2N3d3dPTUyJVZrquL8pomqYQYjgc9no9APA8DwAeHx9fXl5s21ZmpVKJMaYO5GdcXFwg4uvrK023t7eHwyEi0pRzrhwvCp8HIUStVkPE2Wy2s7Pjuq7rur1eL03Tk5MTstF13bIsKITu937fkSLi+/v729ubpmm+739+foZhmOc557zVakkpLcuKomg8HsPiCSCEOD4+TpLk/v6eQsEY63Q6cRx/fHwodY7jfK2ob5VmWVav10ul0vX1NdWoaZqu6zLGOOeGYdBOURR9jdK88trf359MJp1OJwzDarUaBAGdwM3NzWw2I2+iKCLVKoDzlFYqlUajYZpmu90GgCAIbNu2bVvTtDRNm82m53m6rlNKFRnnodVqIWK/37+8vDw4ONjY2PA87+7uDhGjKMrz/PDwkCyllEs0qsFgkCRJFEWIiIjdbhcR0zTNsgwR9/b2AKBcLi9RUQBwdHTU7XaJNAxDok7TtN1ub21tkQ3FbYmKAoB6ve77/tra2vr6+vn5+dPTUxzHV1dX1LGURmppP0Pls1Lh+/7DwwMinp2d0Rsqp6/4Nvqj0QgAOOeqxT0/P0+nUwCQUlarVcaYSqxFSQHANE06xDRNydNarZYkCWNsPB4jYpZlS5NOJhNKQCklJfl0OhVCrK6uJkkCAORBHMeLNhTHcVRvVtSj0Yhz3mw26dbL87xosCioAZODhmHc3t7GcYyIm5ubtKUQgnO+6MX3HQaDQb/fV1P1P/BPpADQaDQAwHEc9WPxf1CMOKVdcXXpfXzfh8KlpGmaEIJyS+EXXIc7GO0j1jYAAAAASUVORK5CYII="  # noqa


@pytest.fixture
def image_np_ndarray():
    return np.array([[1, 2], [3, 4]])
