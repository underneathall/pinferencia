import logging

import numpy as np

from .models import Request

logger = logging.getLogger("uvicorn")


class InputParser:
    def __init__(self, request: Request):
        super().__init__()
        self.inputs = request.inputs

    @property
    def data(self):
        if len(self.inputs) == 1:
            return self.inputs[0].data
        return {_input.name: _input.data for _input in self.inputs}


class OutputParser:
    def __init__(self, raw_data, schema: list = None):
        """Instantiate an Output Parser

        Args:
            raw_data (object): Prediction Result
            schema (dict, optional): metadata["output"
                [
                    {"name": "a", "data": 1, "datatype": "int64"},
                    {"name": "b", "data": 1, "datatype": "int64"},
                ]
        """
        self.raw_data = raw_data
        self.schema = schema

    @property
    def data(self):
        if (
            self.schema
            and len(self.schema) > 1
            and not isinstance(self.raw_data, dict)
        ):
            raise ValueError(
                "Multiple outputs defined, prediction must be a dict."
            )
        if not isinstance(self.raw_data, dict):
            output = self.schema[0] if self.schema else {}
            return [
                {
                    "name": output.get("name") or "default",
                    **self.parse_data(
                        self.raw_data, datatype=output.get("datatype")
                    ),
                }
            ]
        outputs = []
        if self.schema:
            for output in self.schema:
                name = output.get("name")
                if name:
                    outputs.append(
                        {
                            "name": name,
                            **self.parse_data(
                                self.raw_data.pop(name, None),
                                datatype=output.get("datatype"),
                            ),
                        }
                    )
        for k, v in self.raw_data.items():
            outputs.append({"name": k, **self.parse_data(v)})
        return outputs

    def parse_data(self, data, datatype=None):
        npdata = np.array(data)
        parsed_data = {"shape": list(npdata.shape) or -1}
        if datatype:
            try:
                parsed_data["data"] = npdata.astype(datatype).tolist()
                parsed_data["datatype"] = datatype
            except Exception as error:
                parsed_data["data"] = npdata.tolist()
                parsed_data["datatype"] = npdata.dtype.name
                parsed_data[
                    "error"
                ] = f"Failed to convert output to type {datatype}: {error}"
        else:
            parsed_data["data"] = npdata.tolist()
            parsed_data["datatype"] = npdata.dtype.name
        return parsed_data
