from pinferencia import Server


class MyModel:
    def predict(self, data):
        return sum(data)


model = MyModel()

service = Server()
service.register(
    model_name="mymodel",
    model=model,
    entrypoint="predict",
)
