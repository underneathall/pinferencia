import base64
from io import BytesIO
from typing import Dict

import cv2
import paddlehub as hub
from PIL import Image

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

image_generation = hub.Module(name="Photo2Cartoon")


def predict(data: Dict[str, str]):
    base64_img_str = data.get("base64_img_str")
    path = data.get("path")
    images = [cv2.imread(path)] if path else [base64_str_to_cv2(base64_img_str)]
    result = image_generation.Cartoon_GEN(
        images=images, visualization=True, output_dir="./"
    )
    pil_img = Image.fromarray(result[0])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="image_generation",
    model=predict,
    metadata={"task": task.URL_IMAGE_TO_IMAGE},
)
