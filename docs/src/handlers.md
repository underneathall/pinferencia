# Handlers

## BaseHandler

**BaseHandler** is only an abstract base class. You can't use it directly.

Let's Take a look at some of its functions:

```python linenums="1"
class BaseHandler(abc.ABC):

    def preprocess(self, data: object, parameters: object = None):
        return data # (1)

    def postprocess(self, data: object, parameters: object = None):
        return data # (1)

    @abc.abstractmethod
    def predict(self, data: object): # (2)
        return NotImplemented

    @abc.abstractmethod
    def load_model(self):
        return NotImplemented # (2)
```

1. The default codes do nothing. You can override this function to provide your own preprocessing codes.

2. You need to implement this function. Model can be accessed by `self.model`, the entrypoint registered can be accessed by `self.entrypoint`.

3. You need to implement this function. Model path can be accessed by `self.model_path`

## PickleHandler

The default handler is **PickleHandler**.

```python linenums="1"
class PickleHandler(BaseHandler):
    """Pickle Handler for Models Saved through Pickle"""

    def predict(self, data: object):
        if not getattr(self, "model", None):
            raise Exception("Model is not loaded.")
        predict_func = (
            getattr(self.model, self.entrypoint)
            if self.entrypoint
            else self.model
        )
        return predict_func(data)

    def load_model(self):
        if not getattr(self, "model_path", None):
            raise Exception("Model path not provided.")
        with open(self.model_path, "rb") as f:
            return pickle.load(f)
```