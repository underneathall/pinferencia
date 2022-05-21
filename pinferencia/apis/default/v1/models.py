from typing import Any, List, Optional

from pydantic import BaseModel, Extra


class ModelVersion(BaseModel):
    name: str
    display_name: Optional[str] = ""
    description: Optional[str] = ""
    platform: Optional[str] = ""
    device: Optional[str] = ""
    task: Optional[str] = ""
    input_type: Optional[str] = ""
    output_type: Optional[str] = ""


class Model(BaseModel):
    name: str
    versions: Optional[List[ModelVersion]] = []


class RequestBase(BaseModel, extra=Extra.forbid):
    id: Optional[str] = None
    parameters: Optional[dict] = {}


class Request(RequestBase):
    data: Any


class ResponseBase(BaseModel):
    id: Optional[str] = None
    model_name: str
    model_version: Optional[str] = None
    parameters: Optional[dict] = {}


class Response(ResponseBase):
    data: Any
