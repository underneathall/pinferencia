import base64
from io import BytesIO

from PIL import Image


def pil_image_to_base64_str(image: Image) -> str:
    buffered = BytesIO()
    image.convert("RGB").save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def base64_str_to_pil_image(base64_str: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(base64_str)))
