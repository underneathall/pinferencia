
## Model basic information

> Pyramid-Lite is a lightweight model developed by Baidu in 2018 in PyramBox of Computer Vision id 2018 ECCV. It is based on the main network FaceBoxes, measurement, environment, expression changes, meeting changes and other common problem models. The PaddleHub module is based on WIDER FACE data It can be used for face detection based on self-collected face datasets and Baidu self-collected face datasets, which supports prediction.

Reference：https://github.com/PaddlePaddle/PaddleHub/tree/release/v2.2/modules/image/face_detection/pyramidbox_lite_server


## Sample result example

Enter the file path and the model will give its predictions：

=== "Input"

    Image Source (https://www.pexels.com)

    ![face](/assets/images/examples/paddle/face.jpg){ width="300" }

=== "Output"

    ![face](/assets/images/examples/paddle/face_detector.jpg){ width="300" }

:fontawesome-regular-face-laugh-wink: Let's try it out now


## Prerequisite

### 1、environment dependent

Please visit [dependencies](../../../dependencies/)

### 2、pyramidbox_lite_server dependent

- paddlepaddle >= 1.6.2

- paddlehub >= 1.6.0


### 3、Download the model

```bash
hub install pyramidbox_lite_server
```


## Serve the Model

### Install Pinferencia

First, let's install [Pinferencia](https://github.com/underneathall/pinferencia).

```bash
pip install "pinferencia[streamlit]"
```


### Create app.py

Let's save our predict function into a file `app.py` and add some lines to register it.

```python title="app.py" linenums="1"
import base64

import cv2
import numpy as np
import paddlehub as hub

from pinferencia import Server

face_detector = hub.Module(name="pyramidbox_lite_server")


def base64_str_to_cv2(base64_str: str) -> np.ndarray:
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR
    )


def predict(base64_img_str: str):
    return face_detector.face_detection(
        images=[base64_str_to_cv2(base64_img_str)], visualization=True, output_dir="./"
    )


service = Server()
service.register(model_name="face_detector", model=predict)


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

!!! tips

    The image exists on the service machine, you can enter the relative path of the service file or the absolute path of the file


=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/face_detector/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "{base64 encoded image}"
        }'
    ```

    **Response**

    ```
    {
        "model_name": "face_detector",
        "model_version": "default",
        "data": [
            {
                "data": [
                    {
                        "confidence": 0.9984221458435059,
                        "left": 519,
                        "top": 447,
                        "right": 755,
                        "bottom": 750
                    }
                ],
                "path": "ndarray_time=1655802174713885.0"
            }
        ]
    }
    ```

=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/face_detector/predict",
        headers = {"Content-type": "application/json"},
        json={"data": "{base64 encoded image}"},
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "face_detector",
        "model_version": "default",
        "data": [
            {
                "data": [
                    {
                        "confidence": 0.9984221458435059,
                        "left": 519,
                        "top": 447,
                        "right": 755,
                        "bottom": 750
                    }
                ],
                "path": "ndarray_time=1655802174713885.0"
            }
        ]
    }
    ```

    </div>

---
