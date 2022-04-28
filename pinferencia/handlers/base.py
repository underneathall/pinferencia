import abc
import pickle

from pinferencia.context import PredictContext

__all__ = ["BaseHandler", "PickleHandler"]


class BaseHandler(abc.ABC):
    """Base Abstract Class for Handlers"""

    def __init__(
        self,
        model_path: str = None,
        model: object = None,
        entrypoint: str = None,
        **kwargs
    ):
        super().__init__()
        if model_path is None and model is None:
            raise Exception(
                "At least one of model or model path must be provided."
            )
        self.model_path = model_path
        self.model = model
        self.entrypoint = entrypoint
        self.kwargs = kwargs

    def set_context(self, context: PredictContext):
        """Set the Predict Context of the Request

        Args:
            context (PredictContext): Store the Context Info like
                - API scheme
                - Raw Request JSON Data
        """
        self.context = context

    def process(
        self,
        data: object,
        parameters: object = None,
    ):
        """Process Request Data and Parameters

        Args:
            data (object): Any valid JSON
            parameters (object, optional):
                Parameters in the request. Defaults to None.

        Returns:
            Predictions: Results from the model
        """
        return self.postprocess(
            self.predict(
                self.preprocess(
                    data=data,
                    parameters=parameters,
                ),
            ),
            parameters=parameters,
        )

    def preprocess(self, data: object, parameters: object = None):
        return data

    def postprocess(self, data: object, parameters: object = None):
        return data

    def predict(self, data: object):
        if not getattr(self, "model", None):
            raise Exception("Model is not loaded.")
        predict_func = (
            getattr(self.model, self.entrypoint)
            if self.entrypoint
            else self.model
        )
        return predict_func(data)

    @abc.abstractmethod
    def load_model(self):
        return NotImplemented


class PickleHandler(BaseHandler):
    """Pickle Handler for Models Saved through Pickle"""

    def load_model(self):
        if not getattr(self, "model_path", None):
            raise Exception("Model path not provided.")
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
            return self.model
