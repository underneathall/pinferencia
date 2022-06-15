import base64
from io import BytesIO

import streamlit as st
from PIL import Image

from .base import BaseTemplate


class Template(BaseTemplate):
    title = (
        '<span style="color:salmon;">Image</span> '
        '<span style="color:slategray;">to</span> '
        '<span style="color:lightseagreen;">Image</span>'
    )

    def render(self):
        """Render the Streamlit Frontend"""
        super().render()

        with st.form("Image Upload", clear_on_submit=True):
            uploaded_file = st.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"]
            )
            st.form_submit_button("Upload and Run")

        col1, col2 = st.columns(2)
        col1.markdown(
            '<h3 style="text-align: center;">Input</h3>',
            unsafe_allow_html=True,
        )
        col2.markdown(
            '<h3 style="text-align: center;">Result</h3>',
            unsafe_allow_html=True,
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1.image(image, use_column_width=True)
            base64_img_str = base64.b64encode(uploaded_file.getvalue()).decode()
            with st.spinner("Waiting for result"):
                prediction = self.auto_predict(base64_img_str)
                if isinstance(prediction, list) and prediction:
                    prediction = prediction[0]
                result_image = Image.open(BytesIO(base64.b64decode(prediction)))
                col2.image(result_image)
