# Handlers

## BaseHandler

**BaseHandler** 是一个抽象基础类，你不能直接用它。

不过，我们可以看下它的部分接口，可以让我们拓展使用:

```python title="BaseHandler" linenums="1"
class BaseHandler(abc.ABC):

    def preprocess(self, data: object, parameters: object = None):
        return data # (1)

    def postprocess(self, data: object, parameters: object = None):
        return data # (2)

    def predict(self, data: object):
        if not getattr(self, "model", None):
            raise Exception("Model is not loaded.")
        predict_func = ( # (3)
            getattr(self.model, self.entrypoint)
            if self.entrypoint
            else self.model
        )
        return predict_func(data)

    @abc.abstractmethod
    def load_model(self):
        return NotImplemented # (4)
```

1. 默认代码并没有做任何处理，你可以实现自己的逻辑来做 pre-processing 工作。

2. 默认代码并没有做任何处理，你可以实现自己的逻辑来做 post-processing 工作。

3. 根据 entrypoint 和 model 对象，找到预测函数。模型可以通过 `self.model` 获取, entrypoint 可以通过 `self.entrypoint` 获取。

4. 你需要实现这个方法。 模型路径可以通过 `self.model_path` 获取。

## PickleHandler

默认的 handler 是 **PickleHandler**.

```python title="PickleHandler" linenums="1"
class PickleHandler(BaseHandler):
    """Pickle Handler for Models Saved through Pickle"""

    def load_model(self):
        if not getattr(self, "model_path", None):
            raise Exception("Model path not provided.")
        with open(self.model_path, "rb") as f:
            return pickle.load(f)
```