import logging

from pinferencia.api_manager import BaseAPIManager

from .v1 import router as v1router

logger = logging.getLogger("uvicorn")


class APIManager(BaseAPIManager):
    def register_route(self):
        self.app.include_router(
            v1router,
            prefix="/v1",
            tags=["V1"],
        )
