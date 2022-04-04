import logging

from fastapi import HTTPException

from pinferencia.context import PredictContext

from .repository import DefaultModelRepositoryDir, ModelRepository

logger = logging.getLogger("uvicorn")


class ModelManager:
    __models__ = None
    __model_status__ = None

    def __init__(self, root_dir=DefaultModelRepositoryDir) -> None:
        super().__init__()
        self.repository = ModelRepository(root_dir)

    def predict(
        self,
        model_name: str,
        data: object,
        parameters: object = None,
        version_name: str = None,
        context: PredictContext = None,
    ) -> object:
        if not self.repository.is_ready(model_name, version_name):
            raise HTTPException(
                status_code=400,
                detail="Model is not loaded. Load the model first.",
            )
        handler = self.repository.get_handler(model_name, version_name)
        handler.set_context(context)
        return handler.process(data=data, parameters=parameters)
