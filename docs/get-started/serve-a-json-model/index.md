# Run a JSON Model

Now let's first try something easy to get you familiar with **Pinferecia**.

!!! info "TL,DR"
    It's important for you to understand how to register and serve a model in **Pinferencia**.

    However, if you want to try machine learning model now, you can jump to [Serve Pytorch MNIST Model](../pytorch-mnist)

## Define the JSON Model

Let's create a file named `app.py`.

Below is a JSON Model.

It simply return `1` for input `a`, `2` for input `b`, and `0` for other inputs.

```python title="app.py" linenums="1"
class JSONModel:
    def predict(self, data):
        knowledge = {"a": 1, "b": 2}
        return knowledge.get(data, 0)

```

## Create the Service and Register the Model

First we import `Server` from `pinferencia`, then create an instance and register a instance of our `JSON Model`.

```python title="app.py" linenums="1" hl_lines="1 10 11 12"
from pinferencia import Server


class JSONModel:
    def predict(self, data: str) -> int:
        knowledge = {"a": 1, "b": 2}
        return knowledge.get(data, 0)


model = JSONModel()
service = Server()
service.register(model_name="json", model=model, entrypoint="predict")

```

!!! tip "What are the model_name and entrypoint here?"
    **model_name** is the name you give to the model for later API access.
    Here we give the model a name `json`, and the url for this model is `http://127.0.0.1:8000/v1/models/json`.

    If you have any confusion about the APIs, you can always visit the documentation page mentioned in the next part.


    The **entrypoint** `predict` means we will use the `predict` function of `JSON Model` to predict the data.

## Start the Server

<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Open your browser and visit **http://127.0.0.1:8000**, and now you have an automatically generated API Documentation page!

!!! info "FastAPI and Starlette"
    **Pinferencia** builds on [FastAPI](https://fastapi.tiangolo.com) which is built on [Starlette](https://www.starlette.io).

    Thanks to them, you will have an API with OpenAPI Specification. It means you will have an automatic documentation webpage and client codes can also be generated automatically.

!!! tips
    There are two API documentation endpoints:

    - http://127.0.0.1:8000 or http://127.0.0.1:8000/docs
    - http://127.0.0.1:8000/redoc

You can view the API specifiacations and even **try out** the API by yourself!

![Swagger UI](/assets/images/swagger-ui.jpg)

## Test the API

**Create a `test.py` with the codes below.**

!!! tips
    You need to have `requests` installed.
    ```bash
    pip install requests
    ```

```python title="test.py" linenums="1"
import requests


response = requests.post(
    url="http://localhost:8000/v1/models/json/predict",
    json={"data": "a"},
)
print(response.json())

```

**Run the script and check the result.**

<div class="termy">

```console
$ python test.py
{'model_name': 'json', 'data': 1}
```

</div>

**Now let's add two more inputs and make the print pretty.**

```python title="test.py" linenums="1" hl_lines="3-6 9-11"
import requests

print("|{:^10}|{:^15}|".format("Input", "Prediction"))
print("|{:^10}|{:^15}|".format("-" * 10, "-" * 15))

for character in ["a", "b", "c"]:
    response = requests.post(
        url="http://localhost:8000/v1/models/json/predict",
        json={"data": character},
    )
    print(f"|{character:^10}|{str(response.json()['data']):^15}|")

```

**Run the script again and check the result.**

<div class="termy">

```console
$ python test.py
|  Input   |  Prediction   |
|----------|---------------|
|    a     |       1       |
|    b     |       2       |
|    c     |       0       |
```

</div>