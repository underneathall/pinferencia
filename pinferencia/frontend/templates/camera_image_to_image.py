import base64
from io import BytesIO

import streamlit as st
from PIL import Image

from .base import BaseTemplate


class Template(BaseTemplate):
    title = (
        '<span style="color:salmon;">Camera</span> '
        '<span style="color:slategray;">to</span> '
        '<span style="color:lightseagreen;">Image</span>'
    )

    def render(self):
        """Render the Streamlit Frontend"""
        super().render()
        st.markdown(
            '<h3 style="text-align: center;">Input</h3>',
            unsafe_allow_html=True,
        )

        picture = st.camera_input("")
        st.markdown(
            '<h3 style="text-align: center;">Result</h3>',
            unsafe_allow_html=True,
        )

        _, col2, _ = st.columns([1, 5, 1])
        if picture is not None:
            base64_img_str = base64.b64encode(picture.getvalue()).decode()
            with st.spinner("Waiting for result"):
                prediction = self.auto_predict(base64_img_str)
                if isinstance(prediction, list) and prediction:
                    prediction = prediction[0]
                result_image = Image.open(BytesIO(base64.b64decode(prediction)))
                col2.image(result_image, use_column_width=True)
