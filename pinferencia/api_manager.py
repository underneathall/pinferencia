import abc
import logging

from fastapi import FastAPI

logger = logging.getLogger("uvicorn")


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
    ) -> list:
        errors = []
        if metadata is not None and not isinstance(metadata, dict):
            error_msg = "metadata is not a dict."
            logger.error(error_msg)
            errors.append(error_msg)
        return errors
