import json

from pinferencia.handlers import BaseHandler


class JsonHandler(BaseHandler):
    def load_model(self):
        with open(self.model_path) as f:
            return json.load(f)

    def predict(self, data):
        return self.model.get(data, 0)
