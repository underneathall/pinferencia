import base64
from io import BytesIO

import cv2
import numpy as np
import paddlehub as hub
from PIL import Image

from pinferencia import Server, task

semantic_segmentation = hub.Module(name="ExtremeC3_Portrait_Segmentation")


def base64_str_to_cv2(base64_str: str) -> np.ndarray:
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR
    )


def predict(base64_img_str: str) -> str:
    images = [base64_str_to_cv2(base64_img_str)]
    result = semantic_segmentation.Segmentation(
        images=images,
        output_dir="./",
        visualization=True,
    )
    pil_img = Image.fromarray(result[0]["result"])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="semantic_segmentation",
    model=predict,
    metadata={"task": task.IMAGE_TO_IMAGE},
)
