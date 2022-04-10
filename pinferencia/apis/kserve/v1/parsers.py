import logging

import numpy as np

from .models import Request

logger = logging.getLogger("uvicorn")


class InputParser:
    def __init__(self, request: Request):
        super().__init__()
        self.inputs = request.instances

    @property
    def data(self):
        return self.inputs


class OutputParser:
    def __init__(self, raw_data):
        """Instantiate an Output Parser

        Args:
            raw_data (object): Prediction Result
        """
        self.raw_data = raw_data

    @property
    def data(self):
        npdata = np.array(self.raw_data)
        return npdata.tolist()
