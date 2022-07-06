from pinferencia.tools import base64_str_to_pil_image, pil_image_to_base64_str
from pinferencia import tools


def test_image_convesion(image_base64_string):
    image = base64_str_to_pil_image(image_base64_string)
    assert image_base64_string == pil_image_to_base64_str(image)


def test_base64_str_to_cv2(image_base64_string, image_np_ndarray, monkeypatch):
    class CV2:

        IMREAD_COLOR = "default"

        def imdecode(*args, **kwargs):
            return image_np_ndarray

    setattr(tools, "cv2", CV2())

    assert tools.base64_str_to_cv2(image_base64_string).any()


def test_cv2_to_base64_str(image_np_ndarray):
    class CV2:
        def imencode(*args, **kwargs):
            return image_np_ndarray

    setattr(tools, "cv2", CV2())

    assert tools.cv2_to_base64_str(image_np_ndarray)
