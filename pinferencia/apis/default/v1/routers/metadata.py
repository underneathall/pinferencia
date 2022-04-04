from typing import List

from fastapi import APIRouter, Request

from pinferencia.apis.default.v1.models import Model, ModelVersion

router = APIRouter()


@router.get("/models", response_model=List[Model])
async def list_models(request: Request):
    return request.app.model.repository.list_models()


@router.get("/models/{model_name}", response_model=List[ModelVersion])
async def list_model_versions(request: Request, model_name: str):
    return request.app.model.repository.list_models(model_name)
