import base64
from io import BytesIO

import streamlit as st
from PIL import Image

from .base import BaseTemplate


class Template(BaseTemplate):
    title = (
        '<span style="color:salmon;">Text</span> '
        '<span style="color:slategray;">to</span> '
        '<span style="color:lightseagreen;">Image</span>'
    )

    def render(self):
        super().render()

        text = st.text_input("Input")
        pred_btn = st.button("Run")

        if pred_btn:
            with st.spinner("Waiting for result"):
                prediction = self.auto_predict(text)
                if isinstance(prediction, list) and prediction:
                    prediction = prediction[0]
                image = Image.open(BytesIO(base64.b64decode(prediction)))
                st.image(image)
