import abc

import streamlit as st

from pinferencia.model_manager import ModelManager


class BaseTemplate(abc.ABC):
    title = "Base Template"

    def __init__(
        self,
        model_name: str,
        model_manager: ModelManager,
        version_name: str = None,
        metadata: dict = None,
    ):
        super().__init__()
        self.model_name = model_name
        self.model_manager = model_manager
        self.version_name = version_name
        if metadata:
            self.metadata = metadata
        else:
            self.metadata = {}

    def render_header(self):
        title = (
            self.metadata["display_name"]
            if self.metadata.get("display_name")
            else self.title
        )
        st.markdown(
            f'<h1 style="text-align: center;">{title}</h1>',
            unsafe_allow_html=True,
        )
        if self.metadata.get("description"):
            st.markdown(self.metadata["description"], unsafe_allow_html=True)

    def render(self):
        self.render_header()

    def predict(self, data, parse_data: bool = True):
        """Call Prediction API

        Args:
            data (Any): Data to be sent to backend

        Returns:
            prediction: predict results

        Example:
            self.predict([1])
            > [2]
            Here if the default api set is used, the backend will receive:
                {
                    "data": [1]
                }
        """
        return self.model_manager.predict(
            model_name=self.model_name,
            data=data,
            version_name=self.version_name,
            parse_data=parse_data,
        )
