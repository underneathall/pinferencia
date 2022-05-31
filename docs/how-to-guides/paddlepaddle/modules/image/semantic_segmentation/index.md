
## Model basic information

> A lightweight portrait segmentation model based on the ExtremeC3 model. For more details, please refer to: [ExtremeC3_Portrait_Segmentation](https://github.com/clovaai/ext_portrait_segmentation) project.

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/semantic_segmentation/ExtremeC3_Portrait_Segmentation

## Sample result example

Enter the file path and the model will give its predictions：

=== "Input"

![image](/assets/images/examples/paddle/seg.jpg)

=== "Output"

![image](/assets/images/examples/paddle/seg_0.png)

![image](/assets/images/examples/paddle/seg_mask_0.png)

:fontawesome-regular-face-laugh-wink: Let's try it out now


## Prerequisite

### 1、environment dependent   

Please visit [dependencies](/ml/paddlepaddle/dependencies/)

### 2、ExtremeC3_Portrait_Segmentation dependent

  - paddlepaddle >= 2.0.0  

  - paddlehub >= 2.0.0


### 3、Download the model

```
hub install ExtremeC3_Portrait_Segmentation
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
import base64
from io import BytesIO

import cv2
import paddlehub as hub
from PIL import Image
from typing import Dict

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

semantic_segmentation = hub.Module(name="ExtremeC3_Portrait_Segmentation")


def predict(data: Dict[str, str]):
    base64_img_str = data.get("base64_img_str")
    path = data.get("path")
    images = [cv2.imread(path)] if path else [base64_str_to_cv2(base64_img_str)]
    result = semantic_segmentation.Segmentation(
        images=images, output_dir="./", visualization=True
    )
    pil_img = Image.fromarray(result[0]["result"])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="semantic_segmentation",
    model=predict,
    metadata={"task": task.URL_IMAGE_TO_IMAGE},
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

    Open http://127.0.0.1:8501, and the template `Url Image To Image` will be selected automatically.

    ![png](/assets/images/examples/paddle/semantic_segmentation.png)

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/semantic_segmentation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "test.jpg"
        }'
    ```

    **Response**

    ```
    {
        "model_name": "semantic_segmentation",
        "model_version": "default",
        "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRo..."
    }
    ```

=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/semantic_segmentation/predict",
        headers = {"Content-type": "application/json"},
        json={"data": "test.jpg"}
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "semantic_segmentation",
        "model_version": "default",
        "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRo..."
    }
    ```

    </div>

---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
