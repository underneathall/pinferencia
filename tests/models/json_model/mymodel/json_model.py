import json


class JSONModel:
    def __init__(self, json_path):
        with open(json_path, "r") as f:
            self.json = json.load(f)

    def predict(self, data):
        return self.json.get(data, 0)
