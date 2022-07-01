import json

import streamlit as st

from pinferencia.frontend.app import Server
from pinferencia.frontend.templates.base import BaseTemplate


class StatTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Numbers</span> '
        '<span style="color:slategray;">Statistics</span>'
    )

    def render(self):
        super().render()
        json_template = "[]"
        col1, col2 = st.columns(2)
        col2.write("Request Preview")
        raw_text = col1.text_area("Raw Data", value=json_template, height=150)
        col2.json(raw_text)

        pred_btn = st.button("Run")
        if pred_btn:
            with st.spinner("Wait for result"):
                prediction = self.predict(json.loads(raw_text))
            st.write("Statistics")

            result_col1, result_col2, result_col3 = st.columns(3)
            result_col1.metric(label="Max", value=prediction.get("max"))
            result_col2.metric(label="Min", value=prediction.get("min"))
            result_col3.metric(label="Mean", value=prediction.get("mean"))


backend_address = "http://127.0.0.1:8000"

service = Server(
    backend_server=f"{backend_address}",
    custom_templates={"Stat": StatTemplate},
)
