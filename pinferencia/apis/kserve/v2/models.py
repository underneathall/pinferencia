from typing import Any, List, Optional, Union

from pydantic import BaseModel, Extra, validator


class Input(BaseModel, extra=Extra.forbid):
    name: Optional[str] = None
    parameters: Optional[dict] = {}
    data: Any
    shape: Optional[Union[List[int], int]] = []
    datatype: Optional[str] = None


class Output(BaseModel):
    name: Optional[str] = None
    parameters: Optional[dict] = {}
    data: Any
    shape: Optional[Union[List[int], int]] = []
    datatype: Optional[str] = None
    error: Optional[str]


class ModelVersion(BaseModel):
    name: str
    platform: Optional[str] = ""
    inputs: Optional[List[Input]] = []
    outputs: Optional[List[Output]] = []


class Model(BaseModel):
    name: str
    versions: Optional[List[ModelVersion]] = []
    platform: Optional[str] = ""
    inputs: Optional[List[Input]] = []
    outputs: Optional[List[Output]] = []


class Request(BaseModel, extra=Extra.forbid):
    id: Optional[str] = None
    parameters: Optional[dict] = {}
    inputs: List[Input]

    @validator("inputs")
    def validate_multiple_inputs(cls, v):
        if len(v) > 1:
            for _input in v:
                if not _input.name:
                    raise ValueError(
                        "Input name should be provided given multiple inputs."
                    )
        return v


class Response(BaseModel):
    id: Optional[str] = None
    model_name: str
    model_version: Optional[str] = None
    parameters: Optional[dict] = {}
    outputs: List[Output]
