

## Model basic information

> MobileNet V2 is a lightweight convolutional neural network. On the basis of MobileNet, it has made two major improvements: Inverted Residuals and Linear bottlenecks. The PaddleHub Module is trained on Baidu's self-built animal dataset and can be used for image classification and feature extraction. Currently, it supports the classification and recognition of 7978 animals. Details of the model can be found in the [paper](https://arxiv.org/pdf/1801.04381.pdf).

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/face_detection/pyramidbox_lite_server


## Sample result example

Enter the file path and the model will give its predictions：

=== "Input"

Image Source (https://www.pexels.com)

![animal](/assets/images/examples/paddle/animal.jpg)

=== "Output"

`松鼠`

:fontawesome-regular-face-laugh-wink: Let's try it out now



## Prerequisite

### 1、environment dependent  

Please visit [dependencies](/ml/paddlepaddle/dependencies/)

### 2、mobilenet_v2_animals dependent  

  - paddlepaddle >= 1.6.2  

  - paddlehub >= 1.6.0


### 3、Download the model

```
hub install pyramidbox_lite_server
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
from typing import Dict

import cv2
import paddlehub as hub

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

classifier = hub.Module(name="mobilenet_v2_animals")


def predict(data: Dict[str, str]):
    base64_img_str = data.get("base64_img_str")
    path = data.get("path")
    images = [cv2.imread(path)] if path else [base64_str_to_cv2(base64_img_str)]
    return classifier.classification(images=images)


service = Server()
service.register(
    model_name="classifier",
    model=predict,
    metadata={"task": task.URL_IMAGE_TO_TEXT},
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

!!! tips

    The image exists on the service machine, you can enter the relative path of the service file or the absolute path of the file


=== "UI"

    Open http://127.0.0.1:8501, and the template `Url Image To Text` will be selected automatically.

    ![png](/assets/images/examples/paddle/image_classification.png)

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/classifier/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": {"path": "animal.jpg"}
        }'
    ```

    **Response**

    ```
    {
        "model_name": "classifier",
        "data": [
            {
                "松鼠": 0.9506056308746338
            }
        ]
    }
    ```

=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/classifier/predict",
        headers = {"Content-type": "application/json"},
        json={"data": {"path": "animal.jpg"}}
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "classifier",
        "data": [
            {
                "松鼠": 0.9506056308746338
            }
        ]
    }
    ```

    </div>

---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
