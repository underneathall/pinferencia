import importlib

from fastapi import FastAPI

from .model_manager import ModelManager


class Server(FastAPI):
    model = None

    def __init__(self, api="default", model_dir: str = None, **kwargs) -> None:
        fastapi_kwargs = {
            "title": "Pinferencia",
            "version": "0.1.0a3",
        }
        fastapi_kwargs.update(kwargs)
        super().__init__(**fastapi_kwargs)
        api_module = importlib.import_module(
            f".apis.{api}",
            package="pinferencia",
        )

        self.api_manager = api_module.APIManager(self)
        self.api_manager.register_route()
        self.model = ModelManager()
        self.model.repository.set_root_dir(model_dir)

    def register(
        self,
        model_name: str,
        model: object,
        version_name: str = None,
        entrypoint: str = None,
        metadata: dict = None,
        handler: object = None,
        load_now: bool = True,
    ) -> None:
        errors = self.api_manager.validate_model_metadata(
            model_name=model_name,
            metadata=metadata,
            version_name=version_name,
        )
        if errors:
            raise Exception(f"Registration Failed: {errors}")
        self.model.repository.register(
            model_name=model_name,
            model=model,
            version_name=version_name,
            entrypoint=entrypoint,
            metadata=metadata,
            handler=handler,
            load_now=load_now,
        )
