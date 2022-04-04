import logging

from pydantic import ValidationError

from pinferencia.api_manager import BaseAPIManager

from .v1 import router as v1router
from .v2 import router as v2router
from .v2.models import ModelVersion

logger = logging.getLogger("uvicorn")


class APIManager(BaseAPIManager):
    def register_route(self):
        self.app.include_router(
            v1router,
            prefix="/v1",
            tags=["V1"],
        )
        self.app.include_router(
            v2router,
            prefix="/v2",
            tags=["V2"],
        )

    def validate_model_metadata(
        self, model_name: str, metadata: object, version_name: str = None
    ) -> str:
        metadata = {} if metadata is None else metadata
        errors = []
        errors.append(
            self.validate_v2_metadata(model_name=model_name, metadata=metadata)
        )
        return [e for e in errors if e]

    def validate_v2_metadata(self, model_name: str, metadata: dict):
        try:
            assert isinstance(metadata, dict)
            ModelVersion(
                name=model_name,
                platform=metadata.get("platform", ""),
                inputs=metadata.get("inputs", []),
                outputs=metadata.get("outputs", []),
            )
        except AssertionError as error:
            error_msg = "metadata is not a dict."
            logger.exception(error)
            logger.error(error_msg)
            return error_msg
        except ValidationError as error:
            logger.exception("Failed to pass kserve v2 metadata validation")
            return error
