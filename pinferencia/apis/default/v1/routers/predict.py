from fastapi import APIRouter, Request

from pinferencia.apis.default.v1.config import SCHEME
from pinferencia.apis.default.v1.models import Request as InferenceRequest
from pinferencia.apis.default.v1.models import Response as InferenceResponse
from pinferencia.context import PredictContext

router = APIRouter()


@router.post(
    "/models/{model_name}/predict",
    response_model=InferenceResponse,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def model_predict(
    request: Request,
    model_name: str,
    inference_request: InferenceRequest,
):
    return {
        "id": inference_request.id,
        "model_name": model_name,
        "data": request.app.model.predict(
            model_name,
            data=inference_request.data,
            parameters=inference_request.parameters,
            context=PredictContext(
                scheme=SCHEME, request_data=inference_request.dict()
            ),
        ),
    }


@router.post(
    "/models/{model_name}/versions/{version_name}/predict",
    response_model=InferenceResponse,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def model_version_predict(
    request: Request,
    model_name: str,
    version_name: str,
    inference_request: InferenceRequest,
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
