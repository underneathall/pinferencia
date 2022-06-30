import base64

import streamlit as st
from PIL import Image

from pinferencia.frontend.app import Server
from pinferencia.frontend.templates.base import BaseTemplate
from pinferencia.frontend.templates.utils import display_text_prediction


class SumMnistTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Sum</span> '
        '<span style="color:slategray;">MNIST</span> '
    )

    def render(self):
        super().render()

        col1, col2 = st.columns(2)
        with col1.form("First Image", clear_on_submit=True):
            first_number = col1.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"], key="1"
            )

        with col2.form("Second Image", clear_on_submit=True):
            second_number = col2.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"], key="2"
            )

        st.markdown("##### Sum of the two digits:")
        images = []
        if first_number is not None:
            image1 = Image.open(first_number)
            col1.image(image1, use_column_width=True)
            images.append(base64.b64encode(first_number.getvalue()).decode())

        if second_number is not None:
            image1 = Image.open(second_number)
            col2.image(image1, use_column_width=True)
            images.append(base64.b64encode(second_number.getvalue()).decode())

        if first_number and second_number:
            with st.spinner("Waiting for result"):
                prediction = self.predict(images)
                display_text_prediction(prediction, component=st)


backend_address = "http://127.0.0.1:8000"

service = Server(
    backend_server=f"{backend_address}",
    custom_templates={"Sum Mnist": SumMnistTemplate},
)
