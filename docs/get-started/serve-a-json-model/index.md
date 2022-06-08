# Run a JSON Model

Now let's first try something easy to get you familiar with **Pinferecia**.

!!! info "TL;DR"
    It's important for you to understand how to register and serve a model in **Pinferencia**.

    However, if you want to try machine learning model now, you can jump to [Serve Pytorch MNIST Model](../pytorch-mnist)

## Define the JSON Model

Let's create a file named `app.py`.

Below is a JSON Model.

It simply return `1` for input `a`, `2` for input `b`, and `0` for other inputs.

```python title="app.py" linenums="1"
class JSONModel:
    def predict(self, data: str) -> int:
        knowledge = {"a": 1, "b": 2}
        return knowledge.get(data, 0)

```

## Create the Service and Register the Model

First we import `Server` from `pinferencia`, then create an instance and register a instance of our `JSON Model`.

```python title="app.py" linenums="1" hl_lines="1 10 11 12"
from pinferencia import Server, task


class JSONModel:
    def predict(self, data: str) -> int:
        knowledge = {"a": 1, "b": 2}
        return knowledge.get(data, 0)


model = JSONModel()
service = Server()
service.register(
    model_name="json",  # (1)
    model=model,
    entrypoint="predict",  # (2)
    metadata={"task": task.TEXT_TO_TEXT},  # (3)
)

```

1. The name you'd like to give your model to display in the url.
2. The function to use to perform predictions.
3. Set the default task of this model. The frontend template will be automatically selected for this model according to the task defined here.

!!! tip "What are the model_name, entrypoint and task here?"
    **model_name** is the name you give to the model for later API access.
    Here we give the model a name `json`, and the url for this model is `http://127.0.0.1:8000/v1/models/json`.

    If you have any confusion about the APIs, you can always visit the documentation page mentioned in the next part.


    The **entrypoint** `predict` means we will use the `predict` function of `JSON Model` to predict the data.

    The **task** is the indication what kind of the task the model is performing. The corresponding frontend template will be chosen automatically if the `task` of the model is provided. More details of template can be find at [Frontend Requirements](../../reference/frontend/requirements)

## Start the Server

<div class="termy">

```console
$ pinfer app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Open your browser and visit:

- **http://127.0.0.1:8501** to explore the graphic interface with built-in templates!

![GUI](/assets/images/examples/json-model-gui.png)

- **http://127.0.0.1:8000** to explore the automatically generated API Documentation page!

![Swagger UI](/assets/images/swagger-ui.jpg)

??? info "FastAPI and Starlette"
    **Pinferencia** backends builds on [FastAPI](https://fastapi.tiangolo.com) which is built on [Starlette](https://www.starlette.io).

    Thanks to them, you will have an API with OpenAPI Specification. It means you will have an automatic documentation webpage and client codes can also be generated automatically.

    The default address is at:

    - http://127.0.0.1:8000 or http://127.0.0.1:8000/docs

??? info "Streamlit"
    **Pinferencia** frontend builds on [Streamlit](https://streamlit.io/).

    The default address is at:

    - http://127.0.0.1:8501


## Test the API with `requests` and `Postman`

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
