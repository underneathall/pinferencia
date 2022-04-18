from transformers import pipeline, set_seed

from pinferencia import Server

generator = pipeline("text-generation", model="gpt2")
set_seed(42)


def predict(text):
    return generator(text, max_length=50, num_return_sequences=3)


service = Server()
service.register(model_name="gpt2", model=predict)
