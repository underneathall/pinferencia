from typing import Any, List, Optional

from pydantic import BaseModel, Extra


class ModelVersion(BaseModel):
    name: str
    platform: Optional[str] = ""
    device: Optional[str] = ""


class Model(BaseModel):
    name: str
    versions: Optional[List[ModelVersion]] = []


class Request(BaseModel, extra=Extra.forbid):
    id: Optional[str] = None
    parameters: Optional[dict] = {}
    data: Any


class Response(BaseModel):
    id: Optional[str] = None
    model_name: str
    model_version: Optional[str] = None
    parameters: Optional[dict] = {}
    data: Any
