import abc

import requests
import streamlit as st

from pinferencia.repository import DefaultVersionName


class BaseManager(abc.ABC):
    list_model_tmpl = ""
    list_version_tmpl = ""
    predict_version_tmpl = ""
    doc_tmpl = "{server}/docs"

    def __init__(self, server: str, debug: bool = False):
        """Init the API Manager

        Args:
            server (str): backend server address
            debug (bool, optional): debug model on/off. Defaults to False: off.
        """
        self.server = server
        self.debug = debug

    def _get(self, url: str):
        """GET Backend URL

        Args:
            url (str): target url

        Returns:
            response.json() or response.text: result or error
        """
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return response.json()
        return (
            "Non 200 response from backend: "
            f"[{response.status_code}] {url} {response.text}."
        )

    def _post(self, url: str, json_data: object):
        """POST Backend URL

        Args:
            url (str): target url
            json_data (object): payload

        Returns:
            response.json() or response.text: result or error
        """
        response = requests.post(url, json=json_data, verify=False)
        if response.status_code == 200:
            return response.json()
        return f"Non 200 response from backend: URL: {url}, {response.text}"

    def list(self, model_name: str = None):
        """List Models or Versions

        Args:
            model_name (str, optional): model name. Defaults to None.

        Returns:
            result or error: result or error
        """
        if model_name:
            url = self.list_version_tmpl.format(
                server=self.server,
                model_name=model_name,
            )
        else:
            url = self.list_model_tmpl.format(server=self.server)
        return self._get(url)

    @abc.abstractmethod
    def prepare_request_data(self, data: object):
        return NotImplemented  # pragma: no cover

    @abc.abstractmethod
    def parse_response_data(self, data: object):
        return NotImplemented  # pragma: no cover

    def predict(
        self,
        model_name: str,
        data: object,
        version_name: str = None,
        parse_data: bool = True,
    ):
        """Call Backend Predict API

        Args:
            model_name (str): model name
            data (object): data to predict on
            version_name (str, optional): version name of the model. Defaults to None.

        Returns:
            prediction: paresed prediction
        """
        # get the target url
        version_name = DefaultVersionName if version_name is None else version_name
        url = self.predict_version_tmpl.format(
            server=self.server,
            model_name=model_name,
            version_name=version_name,
        )

        # prepare payload according to the backend api
        request_json_data = self.prepare_request_data(data) if parse_data else data

        # call backend
        response_data = self._post(url=url, json_data=request_json_data)

        # if debug mode is on, display the request and response data
        if self.debug:
            debug_expander = st.expander("Debug")
            doc_url = self.doc_tmpl.format(server=self.server)
            debug_expander.write(f"Predict URL - [Backend API Doc]({doc_url})")
            debug_expander.info(url)
            debug_expander.write("Request Data:")
            self.display_debug_json_data(request_json_data, debug_expander)
            debug_expander.write("Response Data:")
            if isinstance(response_data, str):
                # if the response data is invalid, display as error
                debug_expander.error(response_data)
            else:
                self.display_debug_json_data(response_data, debug_expander)

        # if the response data is invalid, return raw data,
        # otherwise, parse the response data first according to the backend api
        return (
            response_data
            if isinstance(response_data, str) or not parse_data
            else self.parse_response_data(response_data)
        )

    def display_debug_json_data(self, json_data: object, component: object):
        """Display debug data

        Args:
            json_data (object): json data to display
            component (st component): streamlit component to show the data
        """
        if len(str(json_data)) > 500:
            component.warning("The JSON body is too large to display.")
            component.code(body=str(json_data)[:500] + "...", language="text")
        else:
            component.json(json_data)
