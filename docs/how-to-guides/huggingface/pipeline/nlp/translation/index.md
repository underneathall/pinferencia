# Google T5 Translation as a Service with Just 7 lines of Codes

What is T5? Text-To-Text Transfer Transformer (T5) from Google gives the power of translation.

![translate](/assets/images/examples/translate-home.png)

In the article, we will deploy Google T5 model as a REST API service. Difficult? What about I’ll tell you: you just need to write 7 lines of codes?

## Install Dependencies

### HuggingFace

```bash
pip install "transformers[torch]"
```

If it doesn’t work, please visit [Installation](https://huggingface.co/docs/transformers/installation) and check their official documentations.

### Pinferencia

```bash
pip install "pinferencia[streamlit]"
```

## Define the Service

First let’s create the app.py to define the service:

```python title="app.py" linenums="1"
from transformers import pipeline

from pinferencia import Server, task

t5 = pipeline(model="t5-base", tokenizer="t5-base")


def translate(text: list) -> list:
    return [res["translation_text"] for res in t5(text)]


service = Server()
service.register(model_name="t5", model=translate, metadata={"task": task.TRANSLATION})
```

## Start the Service

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

## Test the Service

=== "UI"

    Open http://127.0.0.1:8501, and the template `Translation` will be selected automatically.

    ![UI](/assets/images/examples/huggingface/t5.jpg)

=== "Curl"

    ```bash
    curl -X 'POST' \
        'http://localhost:8000/v1/models/t5/predict' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "parameters": {},
        "data": ["translate English to German: Good morning, my love."]
    }'
    ```

    Result:

    ```json
    {
        "model_name": "t5",
        "data": ["translation_text": "Guten Morgen, liebe Liebe."]
    }
    ```

=== "Python requests"

    ```python title="test.py" linenums="1"
    import requests

    response = requests.post(
        url="http://localhost:8000/v1/models/gpt2/predict",
        json={
            "data": ["translate English to German: Good morning, my love."]
        },
    )
    print("Prediction:", response.json()["data"])
    ```

    Run `python test.py` and print the result:

    ```
    Prediction: ["Guten Morgen, liebe Liebe."]
    ```

---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
