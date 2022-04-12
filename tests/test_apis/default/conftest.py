import pytest

from pinferencia import Server


@pytest.fixture(scope="function")
def json_model_default_service(json_model):
    service = Server(api="default")
    service.register(
        model_name="json",
        model=json_model,
        entrypoint="predict",
        metadata={},
    )
    service.register(
        model_name="json",
        model=json_model,
        version_name="v1",
        entrypoint="predict",
        metadata={},
    )
    return service


@pytest.fixture(scope="function")
def json_model_with_path_default_service(
    json_model_dir,
    json_model_path,
    json_model_handler,
):
    service = Server(api="default", model_dir=json_model_dir)
    service.register(
        model_name="json",
        model=json_model_path,
        handler=json_model_handler,
        entrypoint="predict",
        metadata={},
        load_now=False,
    )
    service.register(
        model_name="json",
        model=json_model_path,
        handler=json_model_handler,
        version_name="v1",
        entrypoint="predict",
        metadata={},
        load_now=False,
    )
    service.register(
        model_name="json",
        model=json_model_path,
        handler=json_model_handler,
        version_name="loaded",
        entrypoint="predict",
        metadata={},
    )
    return service


@pytest.fixture(scope="function")
def add_substract_model_default_service():
    from pinferencia import Server

    class MyModel:
        def add(self, data):
            return data[0] + data[1]

        def substract(self, data):
            return data[0] - data[1]

    model = MyModel()

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
        version_name="add",  # (1)
        entrypoint="add",  # (3)
    )
    service.register(
        model_name="mymodel",
        model=model,
        version_name="substract",  # (2)
        entrypoint="substract",  # (4)
    )
    return service
