from .base import BaseManager


class APIManager(BaseManager):

    # TODO: use api router url_of
    list_model_tmpl = "{server}/v1/models"
    list_version_tmpl = list_model_tmpl + "/{model_name}"
    predict_version_tmpl = (
        "{server}/v1/models/{model_name}/versions/{version_name}/predict"
    )

    def prepare_request_data(self, data: object):
        return {"data": data}

    def parse_response_data(self, data: object):
        return data["data"]
