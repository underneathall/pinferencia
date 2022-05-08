import importlib
import time

import streamlit as st

from pinferencia.frontend.config import (
    DEFAULT_DETAIL_DESCRIPTION,
    DEFAULT_SHORT_DESCRIPTION,
)
from pinferencia.task import BUILT_IN_TASKS

from .api_manager import APISet
from .model_manager import ModelManager


class Server:
    def __init__(
        self,
        backend_server: str,
        title: str = None,
        short_description: str = DEFAULT_SHORT_DESCRIPTION,
        detail_description: str = DEFAULT_DETAIL_DESCRIPTION,
        custom_templates: dict = None,
        api_set: set = APISet.DEFAULT,
    ):
        """Frontend Server

        Args:
            backend_server (str): backend server address
            title (str, optional): title of the app. Defaults to None.
            short_description (str, optional):
                short description. Defaults to None.
            detail_description (str, optional):
                detailed description. Defaults to None.
            custom_templates (dict, optional):
                custom template, key is the name, value is the template class.
                Defaults to None.
        """
        self.backend_server = backend_server
        self.title = title if title else "Pinferencia"
        self.short_description = short_description
        self.detail_description = detail_description
        if custom_templates and isinstance(custom_templates, dict):
            self.custom_templates = custom_templates
        else:
            self.custom_templates = {}
        self.model_manager = ModelManager(
            backend_server=self.backend_server,
            api_set=api_set,
        )
        self.render()
        hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            footer:after {
                content:'Made with Pinferencia and Streamlit';
                visibility: visible;
                display: block;
            }
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    def get_task_options(self) -> list:
        task_options = []
        task_options += BUILT_IN_TASKS
        if self.custom_templates:
            task_options += list(self.custom_templates.keys())
        return task_options

    def get_models(self) -> list:
        warning_container = st.empty()
        error = None
        for i in range(10):
            warning_container.info(
                f"Backend is starting. Connecting to backend, attempt: {i + 1} / 10"
            )
            try:
                models = [m["name"] for m in self.model_manager.list()]
                warning_container.empty()
                return models
            except Exception as exc:
                error = exc
                if i < 9:
                    time.sleep(5)
        st.warning(
            "Please check if the backend is running, " "and refresh the page manually."
        )
        with st.expander("Detail"):
            st.error(error)
        return []

    def render(self):
        """Render the page"""
        # prepare upper right corner menu items and page configs
        menu_items = {
            "Get Help": "https://github.com/underneathall/pinferencia/issues",  # noqa
            "Report a bug": "https://github.com/underneathall/pinferencia/issues",  # noqa
            "About": self.detail_description,
        }

        st.set_page_config(
            layout="centered",
            initial_sidebar_state="auto",
            page_title=self.title,
            menu_items=menu_items,
        )

        # render sidebar header
        st.sidebar.title(self.title)
        st.sidebar.markdown(self.short_description)

        # retrieve models from backend
        models = self.get_models()

        # render the model select box
        model_name = st.sidebar.selectbox(
            label="Select the Model",
            options=models,
        )

        # retrieve model version metadata from backend
        versions = (
            {v["name"]: v for v in self.model_manager.list(model_name)}
            if model_name
            else {}
        )

        # render the version select box
        version_name = st.sidebar.selectbox(
            label="Select the Version",
            options=versions,
        )

        # load built-in and custom task options
        task_options = self.get_task_options()

        # if a version is selected
        if version_name:
            # try to read the task of this model version
            version_task = versions[version_name].get("task")
            select_box_kwargs = {
                "label": "Select the Task",
                "options": task_options,
                "format_func": lambda x: x.replace("_", " ").title(),
            }

            # if the task of this model version is defined,
            # select it by default.
            # otherwise, select the first task
            if version_task:
                try:
                    select_box_kwargs["index"] = task_options.index(version_task)
                except ValueError:
                    pass
            task = st.sidebar.selectbox(**select_box_kwargs)

            # if debug mode is enabled, set the api manager to debug mode
            if st.sidebar.checkbox("Debug"):
                self.model_manager.api_manager.debug = True

            # first looking for the selected task type in custom templates,
            # then the built-in templates
            if task in self.custom_templates:
                tmpl_cls = self.custom_templates[task]
            else:
                tmpl_module = importlib.import_module(
                    f".frontend.templates.{task}",
                    package="pinferencia",
                )
                tmpl_cls = tmpl_module.Template

            # initialize the template and render
            tmpl = tmpl_cls(
                model_name=model_name,
                version_name=version_name,
                model_manager=self.model_manager,
                metadata=versions[version_name],
            )
            tmpl.render()
