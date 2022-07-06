

## Model basic information

> This Module is a word segmentation network (bidirectional GRU) built by jieba using the PaddlePaddle deep learning framework. At the same time, it also supports jieba's traditional word segmentation methods, such as precise mode, full mode, search engine mode and other word segmentation modes. The usage methods are consistent with jieba.

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/lexical_analysis/jieba_paddle


## Sample result example

=== "Input"

    ```
    "今天天气真好"
    ```

=== "Output"

    ```
    ['今天', '是', '个', '好日子']
    ```

:fontawesome-regular-face-laugh-wink: Let's try it out now


## Prerequisite

### 1、environment dependent  

Please visit [dependencies](/ml/paddlepaddle/dependencies/)

### 2、jieba_paddle dependent  

  - paddlepaddle >= 1.8.0 

  - paddlehub >= 1.8.0

### 3、Download the model

```
hub install jieba_paddle
```


## Serve the Model

### Install Pinferencia

First, let's install [Pinferencia](https://github.com/underneathall/pinferencia).

```bash
pip install "pinferencia[uvicorn]"
```

### Create app.py

Let's save our predict function into a file `app.py` and add some lines to register it.

```python title="app.py" linenums="1"
import paddlehub as hub

from pinferencia import Server, task

lexical_analysis = hub.Module(name="jieba_paddle")


def predict(text: str):
    return lexical_analysis.cut(text, cut_all=False, HMM=True)


service = Server()
service.register(
    model_name="lexical_analysis", model=predict, metadata={"task": task.TEXT_TO_TEXT}
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

### Test the 

=== "UI"

    Open http://127.0.0.1:8501, and the template `Text to Text` will be selected automatically.

    ![png](/assets/images/examples/paddle/lexical_analysis.png)

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/lexical_analysis/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "今天天气真好"
        }'
    ```

    **Response**

    ```
    {
        "model_name": "lexical_analysis",
        "data": [
            "今天",
            "天气",
            "真好"
        ]
    }
    ```


=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/lexical_analysis/predict",
        json={"data": "今天天气真好"}
    )
    print(response.json())
    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "lexical_analysis",
        "data": [
            "今天",
            "天气",
            "真好"
        ]
    }
    ```

    </div>

---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
