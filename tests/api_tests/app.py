from pinferencia import Server


def predict(data: str) -> str:
    return data


service = Server()
service.register(model_name="test", model=predict)
service.register(model_name="test", model=predict, version_name="v1")
