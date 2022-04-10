from fastapi import APIRouter

from pinferencia.apis.default.v1.routers.basic import router as basic_router
from pinferencia.apis.default.v1.routers.management import (
    router as mangement_router,
)

from .metadata import router as metadata_router
from .predict import router as predict_router

router = APIRouter()
router.include_router(basic_router)
router.include_router(metadata_router)
router.include_router(mangement_router)
router.include_router(predict_router)
