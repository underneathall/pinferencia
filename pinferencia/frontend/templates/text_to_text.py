import streamlit as st

from .base import BaseTemplate
from .utils import display_text_prediction


class Template(BaseTemplate):
    title = (
        '<span style="color:salmon;">Text</span> '
        '<span style="color:slategray;">to</span> '
        '<span style="color:lightseagreen;">Text</span>'
    )

    def render(self):
        super().render()

        text = st.text_area("Input")
        pred_btn = st.button("Run")

        if pred_btn:
            with st.spinner("Wait for result"):
                prediction = self.auto_predict(text)
            display_text_prediction(prediction, st)
