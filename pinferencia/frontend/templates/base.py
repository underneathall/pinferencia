import abc

import streamlit as st

from pinferencia.model_manager import ModelManager

from .utils import format_data_with_type_hint_str, is_list_type


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
        if not self.metadata.get("input_type") or not self.metadata.get("output_type"):
            st.warning(
                "Request/response schema of the model service not properly defined."
                " Frontend may not work as expected. Refer to"
                " https://pinferencia.underneathall.app/how-to-guides/schema/ on"
                " how to define the schema of the request and response of the service."
            )

    def render(self):
        self.render_header()

    def predict(self, data: object, parse_data: bool = True):
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

    def auto_predict(self, data: object) -> object:
        # set default type to list
        input_type = (
            self.metadata["input_type"] if self.metadata.get("input_type") else "list"
        )
        output_type = (
            self.metadata["output_type"] if self.metadata.get("output_type") else "list"
        )

        # if the input type hint is a list or typing.List, put the data in a batch
        if is_list_type(input_type):
            data = [data]

        # try to format the data according to the model's input type hint
        try:
            data = format_data_with_type_hint_str(data=data, type_hint_str=input_type)
        except Exception:
            pass

        result = self.predict(data=data)

        # try to format the data according to the model's output type hint
        try:
            result = format_data_with_type_hint_str(
                data=result, type_hint_str=output_type
            )
        except Exception:
            pass

        # if the reuslt is in a non-empty batch
        if (
            isinstance(result, list)
            and is_list_type(input_type)
            and is_list_type(output_type)
            and result
        ):
            return result[0]
        return result
