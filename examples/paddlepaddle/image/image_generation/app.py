import base64
from io import BytesIO

import paddlehub as hub
from PIL import Image

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

image_generation = hub.Module(name="Photo2Cartoon")


def predict(base64_img_str: str) -> str:
    result = image_generation.Cartoon_GEN(
        images=[base64_str_to_cv2(base64_img_str)], visualization=True, output_dir="./"
    )
    pil_img = Image.fromarray(result[0])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="image_generation",
    model=predict,
    metadata={"task": task.IMAGE_TO_IMAGE},
)
