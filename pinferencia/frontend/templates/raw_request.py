import json

import streamlit as st

from .base import BaseTemplate


class Template(BaseTemplate):
    title = (
        '<span style="color:salmon;">Raw</span> '
        '<span style="color:slategray;">Request</span> '
    )

    def render(self):
        super().render()
        json_template = '{\n\t"data": []\n}'
        col1, col2 = st.columns(2)
        col2.write("Request Preview")
        raw_text = col1.text_area("Raw Request", value=json_template, height=150)
        col2.json(raw_text)
        pred_btn = st.button("Run")

        if pred_btn:
            with st.spinner("Wait for result"):
                prediction = self.predict(json.loads(raw_text), parse_data=False)
            st.write("Response")
            st.json(prediction)
