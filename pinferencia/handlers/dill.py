from .base import BaseHandler


class DillHandler(BaseHandler):
    """Pickle Handler for Models Saved through Pickle"""

    def load_model(self):
        try:
            import dill
        except ImportError:
            raise Exception(
                "dill not installed. To install, run: pip install dill"
            )
        if not getattr(self, "model_path", None):
            raise Exception("Model path not provided.")
        with open(self.model_path, "rb") as f:
            self.model = dill.load(f)
            return self.model
