# Welcome to Pinferencia

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/underneathall/pinferencia.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/underneathall/pinferencia/context:python)
[![codecov](https://codecov.io/gh/underneathall/pinferencia/branch/main/graph/badge.svg?token=M7J77E4IWC)](https://codecov.io/gh/underneathall/pinferencia)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pinferencia)

<!-- [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/pinferencia.svg)](https://badge.fury.io/py/pinferencia) -->

## What is Pinferencia?

**Straight forward. Simple. Powerful.**

**Three extra lines and your model goes online**.

**Pinferencia** (`python` + `inference`) aims to provide the simplest way to serve any of your machine learning models with a fully functioning Rest API.

![Pinferencia](/asserts/images/examples/huggingface-vision.png)

## Features

**Pinferencia** features include:

- [x] **Fast to code, fast to go alive**. Minimal codes to write, minimum codes modifications needed. Just based on what you have.
- [x] **100% Test Coverage**: Both statement and branch coverages, no kidding.
- [x] **Easy to use, easy to understand**.
- [x] **Automatic API documentation page**. All API explained in details with online try-out feature. Thanks to [FastAPI](https://fastapi.tiangolo.com) and [Starlette](https://www.starlette.io).
- [x] **Serve any model**, even a single function can be served.

## Try it now!

### Install 

<div class="termy">

```console
$ pip install "pinferencia[uvicorn]"
---> 100%
```

</div>

### Create the App

=== "Any Model"

    ```python title="app.py"
    from pinferencia import Server


    class MyModel:
        def predict(self, data):
            return sum(data)


    model = MyModel()

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
        entrypoint="predict",
    )
    ```

=== "Any Function"

    ```python title="app.py"
    from pinferencia import Server

    def model(data):
        return sum(data)

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
    )
    ```

=== "Scikit-Learn"

    ```python title="app.py"
    import joblib
    import uvicorn

    from pinferencia import Server


    # train your model
    model = "..."

    # or load your model
    model = joblib.load("/path/to/model.joblib") # (1)

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
        entrypoint="predict", # (2)
    )
    ```

    1. For more details, please visit https://scikit-learn.org/stable/modules/model_persistence.html

    2. `entrypoint` is the function name of the `model` to perform predictions.

        Here the data will be sent to the `predict` function: `model.predict(data)`.

=== "PyTorch"

    ```python title="app.py"
    import torch

    from pinferencia import Server


    # train your models
    model = "..."

    # or load your models (1)
    # from state_dict
    model = TheModelClass(*args, **kwargs)
    model.load_state_dict(torch.load(PATH))

    # entire model
    model = torch.load(PATH)

    # torchscript
    model = torch.jit.load('model_scripted.pt')

    model.eval()

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
    )
    ```

    1. For more details, please visit https://pytorch.org/tutorials/beginner/saving_loading_models.html

=== "Tensorflow"

    ```python title="app.py"
    import tensorflow as tf

    from pinferencia import Server


    # train your models
    model = "..."

    # or load your models (1)
    # saved_model
    model = tf.keras.models.load_model('saved_model/model')

    # HDF5
    model = tf.keras.models.load_model('model.h5')

    # from weights
    model = create_model()
    model.load_weights('./checkpoints/my_checkpoint')
    loss, acc = model.evaluate(test_images, test_labels, verbose=2)

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
        entrypoint="predict",
    )
    ```

    1. For more details, please visit https://www.tensorflow.org/tutorials/keras/save_and_load

=== "HuggingFace Transformer"

    ```python title="app.py" linenums="1"
    from transformers import pipeline

    from pinferencia import Server

    vision_classifier = pipeline(task="image-classification")


    def predict(data):
        return vision_classifier(images=data)


    service = Server()
    service.register(model_name="vision", model=predict)

    ```

### Run!

<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

**Hooray**, your service is alive. Go to **http://127.0.0.1:8000/** and have fun.

![Swagger UI](/asserts/images/swagger-ui.jpg)

Remember to come back to our [**Get Started**](/get-started/home) class!
