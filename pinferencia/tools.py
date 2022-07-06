import base64

try:
    import cv2
except ImportError:
    pass
import numpy as np
from io import BytesIO

from PIL import Image


def pil_image_to_base64_str(image: Image) -> str:
    buffered = BytesIO()
    image.convert("RGB").save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def base64_str_to_pil_image(base64_str: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(base64_str)))


def base64_str_to_cv2(base64_str: str) -> np.ndarray:
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR
    )


def cv2_to_base64_str(image: np.ndarray) -> str:
    return base64.b64encode(cv2.imencode(".jpg", image)[1].tostring())
