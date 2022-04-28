from .base import BaseHandler


class JoblibHandler(BaseHandler):
    """Joblib Handler for Models Saved through Joblib"""

    def load_model(self):
        try:
            import joblib
        except ImportError:
            raise Exception(
                "joblib not installed. To install, run: pip install joblib"
            )
        if not getattr(self, "model_path", None):
            raise Exception("Model path not provided.")
        self.model = joblib.load(self.model_path)
        return self.model
