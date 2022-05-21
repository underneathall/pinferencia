import importlib

import streamlit as st

from .api_manager import APISet


class ModelManager:
    # TODO: select API set automatically
    def __init__(self, backend_server: str, api_set: set = APISet.DEFAULT):
        api_manager_module = importlib.import_module(
            f".frontend.api_manager.{api_set}",
            package="pinferencia",
        )
        self.api_manager = api_manager_module.APIManager(server=backend_server)

    @st.cache(ttl=10)
    def list(self, model_name: str = None):
        response_json = self.api_manager.list(model_name=model_name)
        if not isinstance(response_json, list):
            raise Exception(response_json)
        return response_json

    def predict(
        self,
        model_name: str,
        data: object,
        version_name: str = None,
        parse_data: bool = True,
    ) -> object:
        return self.api_manager.predict(
            model_name=model_name,
            data=data,
            version_name=version_name,
            parse_data=parse_data,
        )
