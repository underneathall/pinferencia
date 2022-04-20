import base64
from io import BytesIO

from PIL import Image
from transformers import pipeline

from pinferencia import Server

vision_classifier = pipeline(task="image-classification")


def classify(image_base64_str):
    image = Image.open(BytesIO(base64.b64decode(image_base64_str)))
    return vision_classifier(images=image)


service = Server()
service.register(model_name="vision", model=classify)
