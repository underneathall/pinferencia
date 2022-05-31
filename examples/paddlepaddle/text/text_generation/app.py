import paddlehub as hub

from pinferencia import Server

text_generation = hub.Module(name="ernie_gen_poetry")


def predict(text: list):
    return text_generation.generate(texts=text, beam_width=5)


service = Server()
service.register(model_name="text_generation", model=predict)
