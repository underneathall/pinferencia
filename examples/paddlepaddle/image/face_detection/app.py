import base64

import cv2
import numpy as np
import paddlehub as hub

from pinferencia import Server

face_detector = hub.Module(name="pyramidbox_lite_server")


def base64_str_to_cv2(base64_str: str) -> np.ndarray:
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR
    )


def predict(base64_img_str: str):
    return face_detector.face_detection(
        images=[base64_str_to_cv2(base64_img_str)], visualization=True, output_dir="./"
    )


service = Server()
service.register(model_name="face_detector", model=predict)
