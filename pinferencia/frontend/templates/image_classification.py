from .image_to_text import Template as ImageToTextTemplate


class Template(ImageToTextTemplate):
    title = (
        '<span style="color:deeppink;">Image</span> '
        '<span style="color:slategray;">Classification</span>'
    )
