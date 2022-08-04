
## Model basic information

> This model is encapsulated from [the paddlepaddle version of the photo2cartoon project of Xiaoshi Technology] (https://github.com/minivision-ai/photo2cartoon-paddle).

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/Image_gan/style_transfer/Photo2Cartoon


## Example

=== "Input"

    Image Source (https://www.pexels.com)

    ![face](/assets/images/examples/paddle/face.jpg){ width="300" }

=== "Output"

    ![face](/assets/images/examples/paddle/image_gen_output.jpg)

:fontawesome-regular-face-laugh-wink: Let's try it out now


## Prerequisite

### 1. environment dependent

Please visit [dependencies](../../../dependencies/)

### 2. mobilenet_v2_animals dependent

  - paddlepaddle >= 2.0.0

  - paddlehub >= 2.0.0


### 3. Download the model

```bash
hub install Photo2Cartoon
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
from io import BytesIO

import paddlehub as hub
from PIL import Image

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

image_generation = hub.Module(name="Photo2Cartoon")


def predict(base64_img_str: str) -> str:
    result = image_generation.Cartoon_GEN(
        images=[base64_str_to_cv2(base64_img_str)], visualization=True, output_dir="./"
    )
    pil_img = Image.fromarray(result[0])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="image_generation",
    model=predict,
    metadata={"task": task.IMAGE_TO_IMAGE},
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

    Open http://127.0.0.1:8501, and the template `Url Image To Image` will be selected automatically.

    ![png](/assets/images/examples/paddle/image_generation.jpg)

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/image_generation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "base64 image string"
        }'
    ```

    **Response**

    ```
    {
        "model_name": "image_generation",
        "model_version": "default",
        "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a..."
    }
    ```

=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/image_generation/predict",
        headers = {"Content-type": "application/json"},
        json={"data": "base64 image string"}
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "image_generation",
        "model_version": "default",
        "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a..."
    }
    ```

    </div>

---

Even cooler, go to http://127.0.0.1:8000, and you will have a full documentation of your APIs.

You can also send predict requests just there!
