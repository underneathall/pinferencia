import logging

from pinferencia.api_manager import BaseAPIManager

from .index import router as index_router
from .v1 import router as v1router

logger = logging.getLogger("uvicorn")


class APIManager(BaseAPIManager):
    def register_route(self):
        self.app.include_router(index_router)
        self.app.include_router(
            v1router,
            prefix="/v1",
            tags=["V1"],
        )
