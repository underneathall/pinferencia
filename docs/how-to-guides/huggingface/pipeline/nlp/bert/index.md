Many of you must have heard of `Bert`, or `transformers`.
And you may also know huggingface.

In this tutorial, let's play with its pytorch transformer model and serve it through REST API

## How does the model work?

With an input of an incomplete sentence, the model will give its prediction:

=== "Input"

    ```
    Paris is the [MASK] of France.
    ```

=== "Output"

    ```
    Paris is the capital of France.
    ```

:fontawesome-regular-face-laugh-wink: Let's try it out now

## Prerequisite

Please visit [Dependencies](/ml/huggingface/dependencies/)

## Serve the Model

### Install Pinferencia

First, let's install [Pinferencia](https://github.com/underneathall/pinferencia).

```bash
pip install "pinferencia[streamlit]"
```

### Create app.py

Let's save our predict function into a file `app.py` and add some lines to register it.

```python title="app.py" linenums="1"
from transformers import pipeline

from pinferencia import Server, task

bert = pipeline("fill-mask", model="bert-base-uncased")


def predict(text: str) -> list:
    return bert(text)


service = Server()
service.register(
    model_name="bert",
    model=predict,
    metadata={"task": task.TEXT_TO_TEXT},
)


```

Run the service, and wait for it to load the model and start the server:

=== "Only Backend"

    <div class="termy">

    ```console
    $ uvicorn app:service --reload
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [xxxxx] using statreload
    INFO:     Started server process [xxxxx]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```

    </div>

=== "Frontend and Backend"

    <div class="termy">

    ```console
    $ pinfer app:service --reload

    Pinferencia: Frontend component streamlit is starting...
    Pinferencia: Backend component uvicorn is starting...
    ```

    </div>

### Test the service

=== "Frontend"

    Open http://127.0.0.1:8501, and the template `Text to Text` will be selected automatically.

    ![UI](/assets/images/examples/huggingface/bert.jpg)

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/bert/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "Paris is the [MASK] of France."
        }'
    ```

    **Response**

    ```
    {
        "model_name":"bert",
        "data":"Paris is the capital of France."
    }
    ```

=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/bert/predict",
        json={"data": "Paris is the [MASK] of France."},
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {'model_name': 'bert', 'data': 'Paris is the capital of France.'}
    ```

    </div>


---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
