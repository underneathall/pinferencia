# 注册模型

注册一个模型非常简单:

```python linenums="1"
service.register(
    model_name="mymodel",
    model=model,
    entrypoint="predict",
)
```

??? info "如果我有多个模型，或者有多个版本呢?"

    你可以注册多个模型，每个模型可以有不同的版本:

    ```python linenums="1"
    service.register(
        model_name="my-model",
        model=my_model,
        entrypoint="predict",
    )
    service.register(
        model_name="my-model",
        model=my_model_v1,
        entrypoint="predict",
        version_name="v1,
    )

    service.register(
        model_name="your-model",
        model=your_model,
        entrypoint="predict",
    )
    service.register(
        model_name="your-model",
        model=your_model_v1,
        entrypoint="predict",
        version_name="v1,
    )
    service.register(
        model_name="your-model",
        model=your_model_v2,
        entrypoint="predict",
        version_name="v2,
    )
    ```

## 参数

| 参数 | 类似 | 默认值（如有） | 细节 |
|-----------|------|---------|---------|
| __model_name__ | str | | 模型名称 |
| __model__ | object | | 模型Python对象，或者模型文件路径 |
| __version_name__ | str | None | 版本名称 |
| __entrypoint__ | str | None | 用来预测的函数名称 |
| __metadata__ | dict | None | 模型基础信息 |
| __handler__ | object | None | Hanlder 类 |
| __load_now__ | bool | True | 是否立刻载入模型 |

## 例子

### Model Name

```python linenums="1" hl_lines="9"
from pinferencia import Server


def predict(data):
    return sum(data)

service = Server()
service.register(
    model_name="mymodel",
    model=predict,
)
```

### Model

=== "Model Object"

    ```python linenums="1" hl_lines="14"
    from pinferencia import Server


    class MyModel:
        def predict(self, data):
            return sum(data)


    model = MyModel()

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
        entrypoint="predict
    )
    ```

=== "Function"

    ```python linenums="1" hl_lines="10"
    from pinferencia import Server


    def predict(data):
        return sum(data)

    service = Server()
    service.register(
        model_name="mymodel",
        model=predict,
    )
    ```

### Version名称

没有提供版本名的模型会用 `default` 版本名.

```python linenums="1" hl_lines="14 19"
from pinferencia import Server


def add(data):
    return data[0] + data[1]

def substract(data):
    return data[0] + data[1]

service = Server()
service.register(
    model_name="mymodel",
    model=add,
    version_name="add", # (1)
)
service.register(
    model_name="mymodel",
    model=substract,
    version_name="substract", # (2)
)
```

1. 预测地址在 http://127.0.0.1/v1/models/mymodel/versions/add/predict
2. 预测地址在 http://127.0.0.1/v1/models/mymodel/versions/substract/predict

### Entrypoint

```python linenums="1" hl_lines="19 25"
from pinferencia import Server


class MyModel:
    def add(self, data):
        return data[0] + data[1]

    def substract(self, data):
        return data[0] - data[1]


model = MyModel()

service = Server()
service.register(
    model_name="mymodel",
    model=model,
    version_name="add", # (1)
    entrypoint="add", # (3)
)
service.register(
    model_name="mymodel",
    model=model,
    version_name="substract", # (2)
    entrypoint="substract", # (4)
)
```

1. 预测地址在 http://127.0.0.1/v1/models/mymodel/versions/add/predict
2. 预测地址在 http://127.0.0.1/v1/models/mymodel/versions/substract/predict
3. `add` 函数会被用来预测.
4. `substract` 函数会被用来预测.


### Metadata

#### 默认API

**Pinferencia** 默认metadata架构支持 **platform** 和 **device**

这些信息仅供展示。

These are information for display purpose only.

```python linenums="1" hl_lines="11-14"
from pinferencia import Server


def predict(data):
    return sum(data)

service = Server()
service.register(
    model_name="mymodel",
    model=predict,
    metadata={
        "platform": "Linux",
        "device": "CPU+GPU",
    }
)
```

#### Kserve API

**Pinferencia** 同时支持 **Kserve** API.

对于 Kserve V2, 模型metadata支持:
- platform
- inputs
- outputs

**inputs** 和 **outputs** 会决定模型收到的数据和返回的数据类型.

```python linenums="1" hl_lines="11-25"
from pinferencia import Server


def predict(data):
    return sum(data)

service = Server(api="kserve") # (1)
service.register(
    model_name="mymodel",
    model=predict,
    metadata={
        "platform": "mac os",
        "inputs": [
            {
                "name": "integers", # (2)
                "datatype": "int64",
                "shape": [1],
                "data": [1, 2, 3],
            }
        ],
        "outputs": [
            {"name": "sum", "datatype": "int64", "shape": -1, "data": 6}, # (3)
            {"name": "product", "datatype": "int64", "shape": -1, "data": 6},
        ],
    }
)
```

1. 如果要使用 Kserve API 需要在实例化服务时设置 api="kserve"。
2. 如果请求包含多组数据，只有 `intergers` 数据会被传递给模型。
3. 输出数据会被转换为 `int64`。`datatype` 字段仅支持`numpy` 数据类型. 如果类型转换失败，响应里会多出 `error` 字段。

### Handler

关于Handler的细节，请查看[Handlers](/handlers/index).

```python linenums="1" hl_lines="5-8 18"
from pinferencia import Server
from pinferencia.handlers import PickleHandler


class MyPrintHandler(PickleHandler):

    def predict(self, data):
        print(data)
        return self.model.predict(data)


def predict(data):
    return sum(data)

service = Server()
service.register(
    model_name="mymodel",
    model=predict,
    handler=MyPrintHandler
)
```

### Load Now

```python linenums="1" hl_lines="17"
import joblib

from pinferencia import Server


class JoblibHandler(BaseHandler):
    def load_model(self):
        return joblib.load(self.model_path)


service = Server(model_dir="/opt/models")
service.register(
    model_name="mymodel",
    model="/path/to/model.joblib",
    entrypoint="predict",
    handler=JoblibHandler,
    load_now=True,
)

```
