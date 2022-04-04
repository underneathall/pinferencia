import abc

from fastapi import FastAPI


class BaseAPIManager(abc.ABC):
    app = None

    def __init__(self, app: FastAPI):
        super().__init__()
        self.app = app

    @abc.abstractmethod
    def register_route(self):
        return NotImplemented

    def validate_model_metadata(
        self,
        model_name: str,
        metadata: dict,
        version_name: str = None,
    ) -> str:
        return None
