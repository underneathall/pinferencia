from .base import BaseHandler

__all__ = ["TorchEntireModelHandler", "TorchScriptHandler"]


class TorchBaseHandler(BaseHandler):
    def load_model(self):
        try:
            import torch
        except ImportError:
            raise Exception("pytorch not installed.")
        use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if use_cuda else "cpu")
        self.model = self._load_model()
        return self.model

    def _load_model(self):
        raise NotImplementedError("_load_model Method must be implemented.")


class TorchEntireModelHandler(TorchBaseHandler):
    """TorchEntireModel Handler for Models Saved through TorchEntireModel"""

    def _load_model(self):
        import torch

        if not getattr(self, "model_path", None):
            raise Exception("Model path not provided.")
        model = torch.load(self.model_path, map_location=self.device)
        model.eval()
        return model


class TorchScriptHandler(TorchBaseHandler):
    """TorchScript Handler for Models Saved through TorchScript"""

    def _load_model(self):
        import torch

        if not getattr(self, "model_path", None):
            raise Exception("Model path not provided.")
        model = torch.jit.load(self.model_path, map_location=self.device)
        model.eval()
        return model
