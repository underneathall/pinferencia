# Google T5 Translation as a Service with Just 7 lines of Codes

What is T5? Text-To-Text Transfer Transformer (T5) from Google gives the power of translation.

![translate](/assets/images/examples/translate-home.png)

In the article, we will deploy Google T5 model as a REST API service. Difficult? What about I’ll tell you: you just need to write 7 lines of codes?

![translate](/assets/images/examples/translate-app.png)

## Install Dependencies

### HuggingFace

```bash
pip install "transformers[pytorch]"
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

from pinferencia import Server

t5 = pipeline(model="t5-base", tokenizer="t5-base")


def translate(text: list) -> list:
    return [res["translation_text"] for res in t5(text)]


service = Server()
service.register(model_name="t5", model=translate)
```

## Start the Service

<div class="termy">

```console
$ pinfer app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## Test the Service

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

Even cooler, go to http://127.0.0.1:8501, and you will have an interactive ui.

You can send predict requests just there!
