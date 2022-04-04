"""This is the JSON Model Example in Documentation"""
from pinferencia import Server


class JSONModel:
    def predict(self, data: str) -> int:
        knowledge = {"a": 1, "b": 2}
        return knowledge.get(data, 0)


model = JSONModel()
service = Server()
service.register(model_name="json", model=model, entrypoint="predict")
