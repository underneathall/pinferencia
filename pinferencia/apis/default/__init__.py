import hashlib
import logging
import typing

from fastapi import APIRouter, Request
from pydantic import create_model

from pinferencia.api_manager import BaseAPIManager
from pinferencia.context import PredictContext
from pinferencia.repository import DefaultVersionName, ModelRepository

from .index import router as index_router
from .v1 import router as v1router
from .v1.config import SCHEME
from .v1.models import RequestBase as V1RequestBase
from .v1.models import ResponseBase as V1ResponseBase

logger = logging.getLogger("uvicorn")


class APIManager(BaseAPIManager):
    def register_route(self):
        self.app.include_router(index_router)
        self.app.include_router(
            v1router,
            prefix="/v1",
            tags=["V1"],
        )

        self.request_models = {}
        self.response_models = {}

    def register_model_endpoint(
        self,
        model_name: str,
        model_repository: ModelRepository,
        version_name: str = None,
    ):
        logger.info("Registering Model Endpoint for [%s-%s]", model_name, version_name)

        # url path to register the model
        paths = []
        path = f"/models/{model_name}"
        if version_name:
            paths.append(path + f"/versions/{version_name}/predict")
        else:
            paths.append(path + "/predict")
            paths.append(path + f"/versions/{DefaultVersionName}/predict")

        # get the model type hint schema of the model
        model_schema = model_repository.get_model_schema(
            model_name=model_name,
            version_name=version_name,
        )

        # get the input type and output type of the model entrypoint
        request_type = model_schema.get("input_type") or typing.Any
        response_type = model_schema.get("output_type") or typing.Any

        # set version name to default if it is null
        version_name = version_name or DefaultVersionName

        # unique name to create the pydantic model
        unique_name = (
            hashlib.md5(model_name.encode()).hexdigest()
            + hashlib.md5(version_name.encode()).hexdigest()
        )

        # create request model
        req_model = create_model(
            "V1RequestModel" + unique_name,
            data=(request_type, ...),
            __base__=V1RequestBase,
        )

        # create response model
        resp_model = create_model(
            "V1V1ResponseModel" + unique_name,
            data=(response_type, ...),
            __base__=V1ResponseBase,
        )

        # save the model into api manager
        self.request_models[f"{model_name}-{version_name}"] = req_model
        self.response_models[f"{model_name}-{version_name}"] = resp_model

        # template predict endpoint function to dynamically serve different models
        def predict(
            request: Request,
            inference_request: req_model,
        ):
            return {
                "id": inference_request.id,
                "model_name": model_name,
                "model_version": version_name,
                "data": request.app.model.predict(
                    model_name,
                    data=inference_request.data,
                    parameters=inference_request.parameters,
                    version_name=version_name,
                    context=PredictContext(
                        scheme=SCHEME, request_data=inference_request.dict()
                    ),
                ),
            }

        # register the route and add to the app
        router = APIRouter()
        for path in paths:
            router.add_api_route(
                path,
                predict,
                methods=["post"],
                summary=f"{model_name.title()} {version_name.title()}",
                response_model=resp_model,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
            )
        self.app.include_router(
            router,
            prefix="/v1",
            tags=["V1 - Predict"],
        )
