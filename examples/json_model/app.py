"""This is the JSON Model Example in Documentation"""
from pinferencia import Server


class JSONModel:
    def predict(self, data: list) -> int:
        knowledge = {"a": 1, "b": 2}
        return [knowledge.get(d, 0) for d in data]


model = JSONModel()
service = Server()
service.register(model_name="json", model=model, entrypoint="predict")
