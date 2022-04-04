import pytest

from pinferencia.repository import ModelRepository


def test_success():
    class TestModel:
        def predict(self, data):
            return data

    repository = ModelRepository()
    assert repository.register(
        model_name="test", model=TestModel(), entrypoint="predict"
    )


def test_invalid_entrypoint():
    class TestModel:
        def predict(self, data):
            return data

    repository = ModelRepository()
    with pytest.raises(Exception) as exc:
        repository.register(
            model_name="test", model=TestModel(), entrypoint="invalid"
        )
    assert "[Register] test doesn't implement invalid." in str(exc.value)


def test_invalid_model_name():
    repository = ModelRepository()
    with pytest.raises(Exception) as exc:
        repository.register(
            model_name=[1, 2], model="abc", entrypoint="invalid"
        )
    assert "[Model Register] Invalid model/version name: not a string" in str(
        exc.value
    )


def test_invalid_version_name():
    repository = ModelRepository()
    with pytest.raises(Exception) as exc:
        repository.register(
            model_name="test",
            version_name=[1, 2],
            model="abc",
            entrypoint="invalid",
        )
    assert "[Model Register] Invalid model/version name: not a string" in str(
        exc.value
    )
