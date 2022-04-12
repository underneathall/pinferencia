# Register

Registering a model is as easy as:

```python linenums="1"
service.register(
    model_name="mymodel",
    model=model,
    entrypoint="predict",
)
```

??? info "Register Multiple Model and Multiple Versions?"

    You can register multiple models with multiple versions:

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

## Attributes

| Attribute | Type | Default | Details |
|-----------|------|---------|---------|
| __model_name__ | str | | Name of the model |
| __model__ | object | | Model object or path |
| __version_name__ | str | None | Name of the version |
| __entrypoint__ | str | None | Name of the function to use |
| __metadata__ | dict | None | Metadata of the model |
| __handler__ | object | None | A class to handler model loading and predicting|
| __load_now__ | bool | True | Whether loading the model on registration |

## Examples

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

### Version Name

Model without version name will be registered as `default` version.

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

1. The predicting endpoint will be http://127.0.0.1/v1/models/mymodel/versions/add/predict
2. The predicting endpoint will be http://127.0.0.1/v1/models/mymodel/versions/substract/predict

### Entrypoint

```python linenums="1" hl_lines="19 25"
from pinferencia import Server


class MyModel:
    def add(data):
        return data[0] + data[1]

    def substract(data):
        return data[0] + data[1]


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

1. The predicting endpoint will be http://127.0.0.1/v1/models/mymodel/versions/add/predict
2. The predicting endpoint will be http://127.0.0.1/v1/models/mymodel/versions/substract/predict
3. `add` function of the model will be used to predict.
4. `substract` function of the model will be used to predict.


### Metadata

#### Default API

**Pinferencia** default metadata schema supports **platform** and **device**

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

**Pinference** also supports **Kserve** API.

For Kserve V2, the metadata supports:
- platform
- inputs
- outputs

The **inputs** and **outputs** metadata will determine the data and datatype model received and returned.

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

1. If you want to use kserve API, you need to set api="kserve" when initializing the service.
2. In the request, if there are multiple inputs, only input with name `intergers` will be passed to the model.
3. Output data will be converted into `int64`. The datatype field only supports `numpy` data type. If the data cannot be converted, there will be an extra error field in the output, indicating the reason of the failure.

### Handler

Details of handlers can be found at [Handlers](/handlers/index).

```python linenums="1" hl_lines="5-8 18"
from pinferencia import Server
from pinferencia.handlers import BaseHandler


class MyPrintHandler(BaseHandler):
    def predict(self, data):
        print(data)
        return super().predict(data)


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
