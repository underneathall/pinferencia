from typing import Dict

import cv2
import paddlehub as hub

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

classifier = hub.Module(name="mobilenet_v2_animals")


def predict(data: Dict[str, str]):
    base64_img_str = data.get("base64_img_str")
    path = data.get("path")
    images = [cv2.imread(path)] if path else [base64_str_to_cv2(base64_img_str)]
    return classifier.classification(images=images)


service = Server()
service.register(
    model_name="classifier",
    model=predict,
    metadata={"task": task.URL_IMAGE_TO_TEXT},
)
