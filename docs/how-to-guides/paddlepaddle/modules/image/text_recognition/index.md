
## Model basic information

> The chinese_ocr_db_crnn_mobile Module is used to identify the Chinese characters in the picture, identify the Chinese characters in the text box, and then classify the angle of the detected text box. The final text recognition algorithm adopts CRNN (Convolutional Recurrent Neural Network), namely Convolutional Recurrent Neural Network. This Module is an ultra-lightweight Chinese OCR model that supports direct prediction.

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/text_recognition/chinese_ocr_db_crnn_mobile

## Sample result example

Enter the file path and the model will give its predictions：

=== "Input"

Image Source (https://www.pexels.com)

![price](/assets/images/examples/paddle/price_input.jpg)

=== "Output"

![price](/assets/images/examples/paddle/price_output.jpg)

:fontawesome-regular-face-laugh-wink: Let's try it out now

## Prerequisite

### 1、environment dependent

Please visit [dependencies](../../../dependencies/)

### 2、yolov3_darknet53_vehicles dependent

  - paddlepaddle >= 1.6.2

  - paddlehub >= 1.6.0

### 3、Download the model

```bash
hub install chinese_ocr_db_crnn_mobile
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
from pinferencia import Server

import paddlehub as hub
import cv2

ocr = hub.Module(
    name="chinese_ocr_db_crnn_mobile", enable_mkldnn=True
)


def predict(path: str):
    return ocr.recognize_text(
        images=[cv2.imread(path)],
        visualization=True,
        output_dir="./"
    )


service = Server()
service.register(model_name="ocr", model=predict)

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
        'http://127.0.0.1:8000/v1/models/ocr/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "test.jpg"
        }'
    ```

    **Response**

    ```
    {'model_name': 'text_gencognition', 'model_version': 'default', 'data': [{'save_path': './ndarray_1655277391.4650576.jpg', 'data': [{'text': 'photo', 'confidence': 0.9524916410446167, 'text_box_position': [[1145, 1913], [1243, 1913], [1243, 1934], [1145, 1934]]}, {'text': 'AARON TUAN', 'confidence': 0.9474555850028992, 'text_box_position': [[1236, 1909], [1424, 1909], [1424, 1937], [1236, 1937]]}, {'text': '#makeup ANNA LE', 'confidence': 0.8719193339347839, 'text_box_position': [[1168, 1934], [1424, 1930], [1424, 1960], [1168, 1964]]}, {'text': '#ekip MT RYDER', 'confidence': 0.9155644178390503, 'text_box_position': [[1193, 1962], [1421, 1962], [1421, 1984], [1193, 1984]]}]}]}
    ```

=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/ocr/predict",
        json={"data": "test.jpg"}
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {'model_name': 'text_gencognition', 'model_version': 'default', 'data': [{'save_path': './ndarray_1655277391.4650576.jpg', 'data': [{'text': 'photo', 'confidence': 0.9524916410446167, 'text_box_position': [[1145, 1913], [1243, 1913], [1243, 1934], [1145, 1934]]}, {'text': 'AARON TUAN', 'confidence': 0.9474555850028992, 'text_box_position': [[1236, 1909], [1424, 1909], [1424, 1937], [1236, 1937]]}, {'text': '#makeup ANNA LE', 'confidence': 0.8719193339347839, 'text_box_position': [[1168, 1934], [1424, 1930], [1424, 1960], [1168, 1964]]}, {'text': '#ekip MT RYDER', 'confidence': 0.9155644178390503, 'text_box_position': [[1193, 1962], [1421, 1962], [1421, 1984], [1193, 1984]]}]}]}
    ```

    </div>

---
