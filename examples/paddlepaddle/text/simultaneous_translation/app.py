import paddlehub as hub

from pinferencia import Server

simultaneous_translation = hub.Module(name="transformer_nist_wait_1")


def predict(text: list):
    for t in text:
        print(f"input: {t}")
        result = simultaneous_translation.translate(t)
        print(f"model output: {result}")


service = Server()
service.register(model_name="simultaneous_translation", model=predict)
