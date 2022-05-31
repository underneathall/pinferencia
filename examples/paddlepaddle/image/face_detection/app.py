from pinferencia import Server

import paddlehub as hub
import cv2

face_detector = hub.Module(name="pyramidbox_lite_server")


def predict(path: str):
    return face_detector.face_detection(
        images=[cv2.imread(path)], visualization=True, output_dir="./"
    )


service = Server()
service.register(model_name="face_detector", model=predict)
