import logging
import os
from collections import defaultdict

from fastapi import HTTPException

from .handlers import BaseHandler, PickleHandler

logger = logging.getLogger("uvicorn")

DefaultVersionName = "default"
DefaultModelRepositoryDir = "/opt/models/"


class ModelRepository:
    __models__ = None

    def __init__(self, root_dir: str = DefaultModelRepositoryDir) -> None:
        super().__init__()
        self.set_root_dir(root_dir)
        self.__models__ = defaultdict(dict)

    def set_root_dir(self, root_dir: str):
        self.root_dir = root_dir

    def get_model(self, model_name: str, version_name: str = None) -> object:
        if not self.has_model(
            model_name=model_name,
            version_name=version_name,
        ):
            raise HTTPException(
                status_code=404,
                detail="Model not found.",
            )
        return self.__models__[model_name].get(
            version_name or DefaultVersionName
        )

    def register(
        self,
        model_name: str,
        model: object,
        version_name: str = None,
        metadata: dict = None,
        entrypoint: str = None,
        handler: object = None,
        load_now: bool = True,
    ) -> bool:
        """Register Models

        Args:
            model_name (str): Name of the Model
            model (object): Model Object Implement Prediction Interface
            version_name (str, optional): Name of version. Defaults to None.
            metadata (dict, optional):
                Metadata of the model/version. Defaults to None.
            entrypoint (str, optional):
                Name of the predict function. Defaults to None.
            handler (object, optional): Handler Class. Defaults to None.
            load_now (bool, optional): Load immediately. Defaults to True.

        Raises:
            Exception: Invalid version name
            Exception: Already registered

        Returns:
            bool: Result of the registration
        """
        metadata = metadata or {}
        version_name = version_name or DefaultVersionName
        entrypoint = entrypoint or "__call__"
        if not isinstance(version_name, str) or not isinstance(
            model_name, str
        ):
            raise Exception(
                "[Model Register] Invalid model/version name: not a string"
            )
        if version_name in self.__models__[model_name]:
            raise Exception(
                f"[Model Register] {version_name} already registered."
            )
        self.__models__[model_name][version_name] = {}
        self.__models__[model_name][version_name]["handler"] = (
            handler or PickleHandler
        )
        self.__models__[model_name][version_name]["metadata"] = metadata
        self.__models__[model_name][version_name]["entrypoint"] = entrypoint
        if isinstance(model, str):
            self.__models__[model_name][version_name]["ready"] = False
            self.__models__[model_name][version_name]["path"] = model
            if load_now:
                return self.load_model(model_name, version_name)
        else:
            if not hasattr(model, entrypoint):
                raise Exception(
                    f"[Register] {model_name} doesn't implement {entrypoint}."
                )
            self.__models__[model_name][version_name]["ready"] = True
            self.__models__[model_name][version_name]["object"] = model
        return True

    def get_handler(
        self, model_name: str, version_name: str = None
    ) -> BaseHandler:
        """Get the Model's Handler

        Args:
            model_name (str): Name of the Model
            version_name (str, optional):
                Name of the Version. Defaults to None.

        Returns:
            BaseHandler: An instance of the handle class
        """
        model = self.get_model(model_name, version_name)
        return model.get("handler")(
            model_path=os.path.join(self.root_dir, model.get("path"))
            if model.get("path")
            else None,
            model=model.get("object"),
            entrypoint=model.get("entrypoint"),
        )

    def load_model(self, model_name: str, version_name: str = None) -> bool:
        """Load Model

        Args:
            model_name (str): Name of the Model
            version_name (str, optional):
                Name of the Version. Defaults to None.

        Raises:
            HTTPException: (400, 404)

        Returns:
            bool: Result of the loading
        """
        model = self.get_model(model_name, version_name)
        if model.get("object"):
            raise HTTPException(
                status_code=400,
                detail="Model already loaded.",
            )
        try:
            handler = self.get_handler(model_name, version_name)
            model["object"] = handler.load_model()
            model["ready"] = True
            logger.info(
                "Model [%s] version [%s] is loaded successfully.",
                model_name,
                version_name,
            )
            return True
        except Exception:
            logger.exception(
                "Fail to load model [%s-%s]", model_name, version_name
            )
        return False

    def unload_model(self, model_name: str, version_name: str = None) -> bool:
        model = self.get_model(model_name, version_name)
        if not model.get("object"):
            raise HTTPException(
                status_code=400,
                detail="Model is not loaded.",
            )
        if not model.get("path"):
            raise HTTPException(
                status_code=400,
                detail="Cannot unload model registered without path.",
            )
        model.pop("object")
        model["ready"] = False
        return True

    def has_model(self, model_name: str, version_name: str = None) -> bool:
        if model_name in self.__models__:
            version_name = version_name or DefaultVersionName
            if version_name in self.__models__[model_name]:
                return True
        return False

    def list_models(self, model_name: str = None) -> list:
        if model_name:
            return [
                self.get_metadata(model_name, version_name)
                for version_name in self.__models__[model_name]
            ]
        return [
            {
                "name": model_name,
                "versions": [
                    self.get_metadata(model_name, version_name)
                    for version_name in model_versions
                ],
            }
            for model_name, model_versions in self.__models__.items()
        ]

    def get_metadata(self, model_name: str, version_name: str = None) -> dict:
        """Get model's metadata

        Args:
            model_name (str): Name of the model
            version_name (str, optional):
                Name of the version. Defaults to None.

        Returns:
            dict: Metadata
        """
        version = self.get_model(
            model_name, version_name or DefaultVersionName
        )
        print("version", version)
        metadata = {"name": version_name}
        metadata.update(version.get("metadata", {}))
        return metadata

    def is_ready(self, model_name: str, version_name: str = None) -> bool:
        """Check if the model is ready

        Args:
            model_name (str): Name of the model
            version_name (str, optional):
                Name of the version. Defaults to None.

        Returns:
            bool: Ready or not
        """
        model = self.get_model(
            model_name=model_name,
            version_name=version_name,
        )
        return model["ready"]
