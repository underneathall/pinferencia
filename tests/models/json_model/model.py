import pathlib

from .mymodel.json_model import JSONModel

model_dir = pathlib.Path(__file__).parent.resolve()
model_path = "model.json"
model = JSONModel(f"{model_dir}/model.json")
inference_data = [
    {"request_data": "a", "response_data": 1},
    {"request_data": "b", "response_data": 2},
    {"request_data": "c", "response_data": 3},
    {"request_data": "d", "response_data": 0},
]
metadata = {
    "platform": "mac os",
    "inputs": [
        {
            "name": "integers",
            "datatype": "str",
            "shape": -1,
            "data": "a",
        }
    ],
    "outputs": [{"name": "sum", "datatype": "int64", "shape": -1, "data": 1}],
}
