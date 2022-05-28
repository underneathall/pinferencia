from pinferencia.tools import base64_str_to_pil_image, pil_image_to_base64_str


def test_image_convesion(image_base64_string):
    image = base64_str_to_pil_image(image_base64_string)
    assert image_base64_string == pil_image_to_base64_str(image)
