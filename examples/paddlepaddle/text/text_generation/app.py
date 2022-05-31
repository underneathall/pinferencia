import paddlehub as hub

from pinferencia import Server, task

text_generation = hub.Module(name="ernie_gen_poetry")


def predict(texts: list) -> list:
    return text_generation.generate(texts=texts, beam_width=5)


service = Server()
service.register(
    model_name="text_generation",
    model=predict,
    metadata={"task": task.TEXT_TO_TEXT},
)
