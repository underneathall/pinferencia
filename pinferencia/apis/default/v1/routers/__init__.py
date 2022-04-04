from fastapi import APIRouter

from .basic import router as basic_router
from .management import router as management_router
from .metadata import router as metadata_router
from .predict import router as predict_router

router = APIRouter()

router.include_router(basic_router)
router.include_router(metadata_router)
router.include_router(management_router)
router.include_router(predict_router)
