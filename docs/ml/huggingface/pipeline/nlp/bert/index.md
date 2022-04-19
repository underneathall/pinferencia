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

Cool~ Let's try it out now~

## Prerequisite

Please visit [Dependencies](/ml/huggingface/dependencies/)

## Serve the Model

### Install Pinferencia

First, let's install [Pinferencia](https://github.com/underneathall/pinferencia).

```bash
pip install "pinferencia[uvicorn]"
```

### Create app.py

Let's save our predict function into a file `app.py` and add some lines to register it.

```python title="app.py" linenums="1"
from transformers import pipeline

from pinferencia import Server

bert = pipeline("fill-mask", model="bert-base-uncased")


service = Server()
service.register(model_name="bert", model=lambda text: bert(text))


```

Run the service, and wait for it to load the model and start the server:
<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Test the service

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
 
 
 
