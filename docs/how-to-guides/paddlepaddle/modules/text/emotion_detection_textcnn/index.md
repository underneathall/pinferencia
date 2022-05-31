
## Model basic information

> Emotion Detection (EmoTect for short) focuses on identifying the emotions of users in intelligent dialogue scenes. For user texts in intelligent dialogue scenes, it automatically determines the emotional category of the text and gives the corresponding confidence. The emotional type is divided into positive , Negative, Neutral. The model is based on TextCNN (Multiple Convolutional Kernel CNN model), which can better capture sentence local correlation.

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/sentiment_analysis/emotion_detection_textcnn


## Sample result example

=== "Input"

    ```
    ["今天天气真好", "湿纸巾是干垃圾", "别来吵我"]
    ```

=== "Output"

    ``` 
    [
        {
            'text':'今天天气真好',
            'emotion_label':2,
            'emotion_key':'positive',
            'positive_probs':0.9267,
            'negative_probs':0.0019,
            'neutral_probs':0.0714
        },
        {
            'text':'湿纸巾是干垃圾',
            'emotion_label':1,
            'emotion_key':'neutral',
            'positive_probs':0.0062,
            'negative_probs':0.0042,
            'neutral_probs':0.9896
        },
        {
            'text':'别来吵我',
            'emotion_label':0,
            'emotion_key':'negative',
            'positive_probs':0.0732,
            'negative_probs':0.7791,
            'neutral_probs':0.1477
        }
    ]
    ```

:fontawesome-regular-face-laugh-wink: Let's try it out now


## Prerequisite

### 1、environment dependent  

Please visit [dependencies](/ml/paddlepaddle/dependencies/)

### 2、emotion_detection_textcnn dependent

  - paddlepaddle >= 1.8.0 

  - paddlehub >= 1.8.0

### 3、Download the model

```
hub install emotion_detection_textcnn
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

emotion_detection_textcnn = hub.Module(name="emotion_detection_textcnn")


def predict(text: list):
    return emotion_detection_textcnn.emotion_classify(texts=text)


service = Server()
service.register(
    model_name="emotion_detection_textcnn",
    model=predict,
)

```


Run the service, and wait for it to load the model and start the server:
<div class="termy">

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

</div>


### Test the service

=== "UI"

    Open http://127.0.0.1:8501, and the template `Raw Request` will be selected automatically.

    ![png](/assets/images/examples/paddle/emotion_detection_textcnn.png)

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/emotion_detection_textcnn/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": ["今天天气真好", "湿纸巾是干垃圾", "别来吵我"]
        }'
    ```

    **Response**

    ```
    {
        "model_name": "emotion_detection_textcnn",
        "data": [
            {
                "text": "今天天气真好",
                "emotion_label": 2,
                "emotion_key": "positive",
                "positive_probs": 0.9267,
                "negative_probs": 0.0019,
                "neutral_probs": 0.0714
            },
            {
                "text": "湿纸巾是干垃圾",
                "emotion_label": 1,
                "emotion_key": "neutral",
                "positive_probs": 0.0062,
                "negative_probs": 0.0042,
                "neutral_probs": 0.9896
            },
            {
                "text": "别来吵我",
                "emotion_label": 0,
                "emotion_key": "negative",
                "positive_probs": 0.0732,
                "negative_probs": 0.7791,
                "neutral_probs": 0.1477
            }
        ]
    }
    ```


=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/emotion_detection_textcnn/predict",
        json={"data": ["今天天气真好", "湿纸巾是干垃圾", "别来吵我"]}
    )
    print(response.json())
    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "emotion_detection_textcnn",
        "data": [
            {
                "text": "今天天气真好",
                "emotion_label": 2,
                "emotion_key": "positive",
                "positive_probs": 0.9267,
                "negative_probs": 0.0019,
                "neutral_probs": 0.0714
            },
            {
                "text": "湿纸巾是干垃圾",
                "emotion_label": 1,
                "emotion_key": "neutral",
                "positive_probs": 0.0062,
                "negative_probs": 0.0042,
                "neutral_probs": 0.9896
            },
            {
                "text": "别来吵我",
                "emotion_label": 0,
                "emotion_key": "negative",
                "positive_probs": 0.0732,
                "negative_probs": 0.7791,
                "neutral_probs": 0.1477
            }
        ]
    }
    ```

    </div>

---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
