import base64
from io import BytesIO

import cv2
import paddlehub as hub
from PIL import Image
from typing import Dict

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

semantic_segmentation = hub.Module(name="ExtremeC3_Portrait_Segmentation")


def predict(data: Dict[str, str]):
    base64_img_str = data.get("base64_img_str")
    path = data.get("path")
    images = [cv2.imread(path)] if path else [base64_str_to_cv2(base64_img_str)]
    result = semantic_segmentation.Segmentation(
        images=images, output_dir="./", visualization=True
    )
    pil_img = Image.fromarray(result[0]["result"])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="semantic_segmentation",
    model=predict,
    metadata={"task": task.URL_IMAGE_TO_IMAGE},
)
