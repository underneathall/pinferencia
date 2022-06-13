from transformers import pipeline

from pinferencia import Server, task

bert = pipeline("fill-mask", model="bert-base-uncased")


def predict(text: str) -> list:
    return bert(text)


service = Server()
service.register(
    model_name="bert",
    model=predict,
    metadata={"task": task.TEXT_TO_TEXT},
)
