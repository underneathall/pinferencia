# Welcome to Pinferencia

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/underneathall/pinferencia.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/underneathall/pinferencia/context:python)
[![codecov](https://codecov.io/gh/underneathall/pinferencia/branch/main/graph/badge.svg?token=M7J77E4IWC)](https://codecov.io/gh/underneathall/pinferencia)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pinferencia)

<!-- [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/pinferencia.svg)](https://badge.fury.io/py/pinferencia) -->

## What is Pinferencia?

**Pinferencia** (`python` + `inference`) aims to provide the simplest way to serve any of your machine learning models with a fully functioning Rest API.

**Straight forward. Simple. Powerful.**

<div class="termy">

```console
$ pip install "pinferencia[uvicorn]"
---> 100%
```

</div>

## Features

**Pinferencia** features include:

- [x] **Fast to code, fast to go alive**. Minimal codes needed, minimal transformations needed. Just based on what you have.
- [x] **100% Test Coverage**: Both statement and branch coverages, no kidding.
- [x] **Easy to use, easy to understand**.
- [x] **Automatic API documentation page**. All API explained in details with online try-out feature. Thanks to [FastAPI](https://fastapi.tiangolo.com) and [Starlette](https://www.starlette.io).
- [x] **Serve any model**, even a single function can be served.

## Try it now!

### Create the App

```python title="app.py" linenums="1"
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

Remember to come back to our [**Get Started**](/get-started/home) class!
