from transformers import pipeline

from pinferencia import Server, task

vision_classifier = pipeline(task="image-classification")


def classify(data: str) -> list:
    return vision_classifier(images=data)


service = Server()
service.register(
    model_name="vision", model=classify, metadata={"task": task.TEXT_TO_TEXT}
)
