import base64

import streamlit as st

from pinferencia.frontend.templates.utils import display_text_prediction

from .base import BaseTemplate


class Template(BaseTemplate):
    title = (
        '<span style="color:salmon;">Camera</span> '
        '<span style="color:slategray;">to</span> '
        '<span style="color:lightseagreen;">Text</span>'
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
                display_text_prediction(prediction, component=col2)
