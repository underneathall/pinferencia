from pinferencia import Server

import paddlehub as hub
import cv2

vehicle_detection = hub.Module(name="yolov3_darknet53_vehicles")


def predict(path: str):
    return vehicle_detection.object_detection(
        images=[cv2.imread(path)], visualization=True, output_dir="./"
    )


service = Server()
service.register(model_name="vehicle_detection", model=predict)
