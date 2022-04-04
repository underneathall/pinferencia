from fastapi import APIRouter

from pinferencia.apis.default.v1.routers.basic import router as basic_router
from pinferencia.apis.default.v1.routers.management import (
    router as mangement_router,
)

Scheme = "kservev2"

router = APIRouter()
router.include_router(basic_router)
router.include_router(mangement_router)
