import pytest

from pinferencia import Server, task


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
        version_name="add",
        entrypoint="add",
    )
    service.register(
        model_name="mymodel",
        model=model,
        version_name="substract",
        entrypoint="substract",
    )
    return service


@pytest.fixture(scope="function")
def dummy_model_service():
    def dummy(data: str) -> str:
        return data

    def dummy_v1(data: list) -> list:
        return data

    service = Server()
    service.register(
        model_name="dummy",
        model=dummy,
        metadata={
            "task": task.TEXT_TO_TEXT,
            "display_name": "Dummy Model",
            "description": "This is a dummy model.",
            "device": "CPU",
            "platform": "linux",
        },
    )
    service.register(
        model_name="dummy",
        model=dummy_v1,
        version_name="v1",
        metadata={
            "task": task.TEXT_TO_TEXT,
            "display_name": "Dummy Model V1",
            "description": "This is a dummy model v1.",
        },
    )
    return service


@pytest.fixture(scope="function")
def dummy_model_service_with_decorator():
    service = Server()

    @service.decorators.register(
        model_name="dummy",
        metadata={
            "task": task.TEXT_TO_TEXT,
            "display_name": "Dummy Model",
            "description": "This is a dummy model.",
            "device": "CPU",
            "platform": "linux",
        },
    )
    def dummy(data: str) -> str:
        return data

    @service.decorators.register(
        model_name="dummy",
        version_name="v1",
        metadata={
            "task": task.TEXT_TO_TEXT,
            "display_name": "Dummy Model V1",
            "description": "This is a dummy model v1.",
        },
    )
    def dummy_v1(data: list) -> list:
        return data

    return service
