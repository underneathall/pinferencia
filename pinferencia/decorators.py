from typing import Callable

from fastapi import FastAPI


class AppDecorators:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def register(
        self,
        model_name: str,
        version_name: str = None,
        metadata: dict = None,
    ) -> Callable:
        def _register(model):
            return self.app.register(
                model_name=model_name,
                model=model,
                version_name=version_name,
                metadata=metadata,
            )

        return _register


class AppDecoratorDescriptor:
    def __set_name__(self, owner: object, name: str):
        self.private_name = f"_{name}"

    def __get__(self, obj, obj_type=None):
        if not getattr(obj, self.private_name, None):
            setattr(obj, self.private_name, AppDecorators(obj))
        return getattr(obj, self.private_name)
