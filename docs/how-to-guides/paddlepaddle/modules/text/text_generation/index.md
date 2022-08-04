

## Model basic information

> ERNIE-GEN is a pre-training-fine-tuning framework for generation tasks. For the first time, span-by-span generation tasks are added to the pre-training stage, so that the model can generate a semantically complete segment each time. The exposure bias problem is mitigated by a padding generative mechanism and a noise-aware mechanism in pre-training and fine-tuning. In addition, ERNIE-GEN samples multi-segment-multi-granularity target text sampling strategy, which enhances the correlation between source text and target text, and strengthens the interaction between encoder and decoder. ernie_gen_poetry is fine-tuned on the open source poetry dataset and can be used to generate poetry.

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/text_generation/ernie_gen_poetry

## Sample result example

=== "Input"

    ```json
    ["昔年旅南服，始识王荆州。", "高名出汉阴，禅阁跨香岑。"]
    ```

=== "Output"

    ```json
    [
        [
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，俯仰成春秋。",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与夫子，相逢",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与君别，飘零",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，各在",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，风雨"
        ],
        [
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树林。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树阴。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂林。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏正森。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂阴。"
        ]
    ]
    ```

:fontawesome-regular-face-laugh-wink: Let's try it out now


## Prerequisite

### 1、environment dependent

Please visit [dependencies](../../../dependencies/)

### 2、ernie_gen_poetry dependent

- paddlepaddle >= 2.0.0

- paddlehub >= 2.0.0

- paddlenlp >= 2.0.0

```bash
pip3 install paddlenlp
```

### 3、Download the model

```bash
hub install ernie_gen_poetry
```


## Serve the Model

### Install Pinferencia

First, let's install [Pinferencia](https://github.com/underneathall/pinferencia)。

```bash
pip install "pinferencia[streamlit]"
```

### Create app.py

Let's save our predict function into a file `app.py` and add some lines to register it.

```python title="app.py" linenums="1"
import paddlehub as hub

from pinferencia import Server, task

text_generation = hub.Module(name="ernie_gen_poetry")


def predict(texts: list) -> list:
    return text_generation.generate(texts=texts, beam_width=5)


service = Server()
service.register(
    model_name="text_generation",
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

=== "UI"

    Open http://127.0.0.1:8501, and the template `TEXT_TO_TEXT` will be selected automatically.

    ![png](/assets/images/examples/paddle/text_gen.jpg)

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/text_generation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": ["昔年旅南服，始识王荆州。", "高名出汉阴，禅阁跨香岑。"]
        }'
    ```

    **Response**

    ```
    {
        "model_name": "text_generation",
        "data": [
            [
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，俯仰成春秋。",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与夫子，相逢",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与君别，飘零",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，各在",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，风雨"
            ],
            [
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树阴。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏正森。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂阴。"
            ]
        ]
    }
    ```


=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/text_generation/predict",
        json={"data": ["昔年旅南服，始识王荆州。", "高名出汉阴，禅阁跨香岑。"]}
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "text_generation",
        "data": [
            [
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，俯仰成春秋。",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与夫子，相逢",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与君别，飘零",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，各在",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，风雨"
            ],
            [
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树阴。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏正森。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂阴。"
            ]
        ]
    }
    ```

    </div>

---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
