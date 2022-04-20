from transformers import pipeline

from pinferencia import Server

bert = pipeline("fill-mask", model="bert-base-uncased")


service = Server()
service.register(model_name="bert", model=lambda text: bert(text))
