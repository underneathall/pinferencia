import uvicorn

from pinferencia.app import Server


class SumModel:
    def load(self):
        return True

    def predict(self, data):
        return sum(data)


service = Server()
service.register(
    model_name="abc",
    model=SumModel(),
    entrypoint="predict",
    metadata={
        "platform": "linux",
        "inputs": [
            {
                "name": "integers",
                "datatype": "int64",
                "shape": [2],
                "data": [1, 2],
            }
        ],
        "outputs": [
            {"name": "sum", "datatype": "int64", "shape": -1, "data": 3}
        ],
    },
    load_now=True,
)
service.register(
    model_name="abc",
    version_name="v1",
    model=SumModel(),
    metadata={
        "platform": "linux",
        "inputs": [
            {
                "name": "integers",
                "datatype": "int64",
                "shape": [2],
                "data": [1, 2],
            }
        ],
        "outputs": [
            {"name": "sum", "datatype": "int64", "shape": -1, "data": 3}
        ],
    },
)
service.register(
    model_name="abc",
    version_name="v2",
    model=SumModel(),
    metadata={
        "platform": "linux",
        "inputs": [
            {
                "name": "integers",
                "datatype": "int64",
                "shape": [2],
                "data": [1, 2],
            }
        ],
        "outputs": [
            {"name": "sum", "datatype": "int64", "shape": -1, "data": 3}
        ],
    },
)


class AnyModel:
    def predict(self, data, **kwargs):
        return sum(data)


service.register(
    model_name="abc",
    model=AnyModel(),
    version_name="v3",
    metadata={
        "platform": "mac os",
        "inputs": [
            {
                "name": "integers",
                "datatype": "int64",
                "shape": [2],
                "data": [1, 2],
            }
        ],
        "outputs": [
            {"name": "sum", "datatype": "int64", "shape": -1, "data": 3}
        ],
    },
)

if __name__ == "__main__":
    uvicorn.run(
        service,
        port=8080,
        # app_dir="~/DevSpace/Projects/Kserve-Inference-Server/pinferencia/",
    )
