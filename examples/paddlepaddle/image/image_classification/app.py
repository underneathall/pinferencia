import base64

import cv2
import numpy as np
import paddlehub as hub

from pinferencia import Server, task

classifier = hub.Module(name="mobilenet_v2_animals")


def base64_str_to_cv2(base64_str: str) -> np.ndarray:
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR
    )


def predict(data: list) -> list:
    images = [base64_str_to_cv2(base64_img_str) for base64_img_str in data]
    return classifier.classification(images=images)


service = Server()
service.register(
    model_name="classifier",
    model=predict,
    metadata={"task": task.IMAGE_TO_TEXT},
)
