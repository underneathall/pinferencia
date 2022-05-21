from transformers import pipeline

from pinferencia import Server

t5 = pipeline(model="t5-base", tokenizer="t5-base")


def translate(text: list) -> list:
    return [res["translation_text"] for res in t5(text)]


service = Server()
service.register(model_name="t5", model=translate)
