import pathlib

from pinferencia import Server

from .mymodel.json_model import JSONModel

current_dir = pathlib.Path(__file__).parent.resolve()
service = Server()

service.register(
    model_name="json",
    model=JSONModel(f"{current_dir}/model.json"),
    entrypoint="predict",
    metadata={},
)

service.register(
    model_name="json",
    model=JSONModel(f"{current_dir}/model.json"),
    version_name="v1",
    entrypoint="predict",
    metadata={},
)
