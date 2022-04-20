from transformers import pipeline

from pinferencia import Server

vision_classifier = pipeline(task="image-classification")


def classify(data):
    return vision_classifier(images=data)


service = Server()
service.register(model_name="vision", model=classify)
