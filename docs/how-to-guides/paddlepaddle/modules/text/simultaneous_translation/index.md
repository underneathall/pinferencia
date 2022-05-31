

## Model basic information

> Simultaneous interpretation, that is, translation before the sentence is completed, the goal of simultaneous interpretation is to automate simultaneous interpretation, which can be translated at the same time as the source language, with a delay of only a few seconds.

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/simultaneous_translation/stacl/transformer_nist_wait_1


## Sample result example

=== "Input"

    ```
    [
        "他",
        "他还",
        "他还说",
        "他还说现在",
        "他还说现在正在",
        "他还说现在正在为",
        "他还说现在正在为这",
        "他还说现在正在为这一",
        "他还说现在正在为这一会议",
        "他还说现在正在为这一会议作出",
        "他还说现在正在为这一会议作出安排",
        "他还说现在正在为这一会议作出安排。",
    ]
    ```
=== "Output"

    ```
    input: 他
    model output: he

    input: 他还
    model output: he also

    input: 他还说
    model output: he also said

    input: 他还说现在
    model output: he also said that

    input: 他还说现在正在
    model output: he also said that he

    input: 他还说现在正在为
    model output: he also said that he is

    input: 他还说现在正在为这
    model output: he also said that he is making

    input: 他还说现在正在为这一
    model output: he also said that he is making preparations

    input: 他还说现在正在为这一会议
    model output: he also said that he is making preparations for

    input: 他还说现在正在为这一会议作出
    model output: he also said that he is making preparations for this

    input: 他还说现在正在为这一会议作出安排
    model output: he also said that he is making preparations for this meeting

    input: 他还说现在正在为这一会议作出安排。
    model output: he also said that he is making preparations for this meeting .
    ```

:fontawesome-regular-face-laugh-wink: Let's try it out now


## Prerequisite

### 1、environment dependent  

Please visit [dependencies](/ml/paddlepaddle/dependencies/)

### 2、transformer_nist_wait_1 dependent  

  - paddlepaddle >= 2.1.0

  - paddlehub >= 2.1.0

### 3、Download the model

```
hub install transformer_nist_wait_1
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

from pinferencia import Server

simultaneous_translation = hub.Module(name="transformer_nist_wait_1")


def predict(text: list):
    for t in text:
        print(f"input: {t}")
        result = simultaneous_translation.translate(t)
        print(f"model output: {result}")


service = Server()
service.register(model_name="simultaneous_translation", model=predict)

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
        'http://127.0.0.1:8000/v1/models/simultaneous_translation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": [
                "他",
                "他还",
                "他还说",
                "他还说现在",
                "他还说现在正在",
                "他还说现在正在为",
                "他还说现在正在为这",
                "他还说现在正在为这一",
                "他还说现在正在为这一会议",
                "他还说现在正在为这一会议作出",
                "他还说现在正在为这一会议作出安排",
                "他还说现在正在为这一会议作出安排。",
            ]
        }'
    ```

    **Response**

    on the server page
    ```
    input: 他
    model output: he

    input: 他还
    model output: he also

    input: 他还说
    model output: he also said

    input: 他还说现在
    model output: he also said that

    input: 他还说现在正在
    model output: he also said that he

    input: 他还说现在正在为
    model output: he also said that he is

    input: 他还说现在正在为这
    model output: he also said that he is making

    input: 他还说现在正在为这一
    model output: he also said that he is making preparations

    input: 他还说现在正在为这一会议
    model output: he also said that he is making preparations for

    input: 他还说现在正在为这一会议作出
    model output: he also said that he is making preparations for this

    input: 他还说现在正在为这一会议作出安排
    model output: he also said that he is making preparations for this meeting

    input: 他还说现在正在为这一会议作出安排。
    model output: he also said that he is making preparations for this meeting .
    ```


=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    requests.post(
        url="http://localhost:8000/v1/models/simultaneous_translation/predict",
        json={"data": [
                "他",
                "他还",
                "他还说",
                "他还说现在",
                "他还说现在正在",
                "他还说现在正在为",
                "他还说现在正在为这",
                "他还说现在正在为这一",
                "他还说现在正在为这一会议",
                "他还说现在正在为这一会议作出",
                "他还说现在正在为这一会议作出安排",
                "他还说现在正在为这一会议作出安排。",
            ]}
    )
    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    # on the server page
    input: 他
    model output: he

    input: 他还
    model output: he also

    input: 他还说
    model output: he also said

    input: 他还说现在
    model output: he also said that

    input: 他还说现在正在
    model output: he also said that he

    input: 他还说现在正在为
    model output: he also said that he is

    input: 他还说现在正在为这
    model output: he also said that he is making

    input: 他还说现在正在为这一
    model output: he also said that he is making preparations

    input: 他还说现在正在为这一会议
    model output: he also said that he is making preparations for

    input: 他还说现在正在为这一会议作出
    model output: he also said that he is making preparations for this

    input: 他还说现在正在为这一会议作出安排
    model output: he also said that he is making preparations for this meeting

    input: 他还说现在正在为这一会议作出安排。
    model output: he also said that he is making preparations for this meeting .
    ```

    </div>

---
