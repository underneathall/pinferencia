
In this tutorial, we will explore how to use Hugging Face pipeline, and how to deploy it with [Pinferencia](https://github.com/underneathall/pinferencia) as REST API.

---


## Prerequisite

Please visit [Dependencies](/ml/huggingface/dependencies/)

## Download the model and predict

The model will be automatically downloaded.

```python linenums="1"
from transformers import pipeline
vision_classifier = pipeline(task="image-classification")

vision_classifier(
    images="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"
)
```

![hfimg](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg)

Result:

```python
[{'label': 'lynx, catamount', 'score': 0.4403027892112732},
 {'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor',
  'score': 0.03433405980467796},
 {'label': 'snow leopard, ounce, Panthera uncia',
  'score': 0.032148055732250214},
 {'label': 'Egyptian cat', 'score': 0.02353910356760025},
 {'label': 'tiger cat', 'score': 0.023034192621707916}]
```

Amazingly easy! Now let's try:

## Deploy the model

Without deployment, how could a machine learning tutorial be complete?

First, let's install [Pinferencia](https://github.com/underneathall/pinferencia).

```bash
pip install "pinferencia[streamlit]"
```
Now let's create an app.py file with the codes:

```python title="app.py" linenums="1" hl_lines="3 12-15"
from transformers import pipeline

from pinferencia import Server, task

vision_classifier = pipeline(task="image-classification")


def classify(data: str) -> list:
    return vision_classifier(images=data)


service = Server()
service.register(
    model_name="vision", model=classify, metadata={"task": task.TEXT_TO_TEXT}
)

```

Easy, right?

## Predict

=== "Curl"

    ```bash
    curl --location --request POST 'http://127.0.0.1:8000/v1/models/vision/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"
        }'
    ```

    Result:
    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```

=== "Python requests"

    ```python title="test.py" linenums="1"
    import requests

    response = requests.post(
        url="http://localhost:8000/v1/models/vision/predict",
        json={
            "data": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"  # noqa
        },
    )
    print("Prediction:", response.json()["data"])
    ```

    Run `python test.py` and result:

    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```

Even cooler, go to http://127.0.0.1:8501, and you will have an interactive ui.

You can send predict request just there!

## Improve it

However, using the url of the image to predict sometimes is not always convenient.

Let's modify the `app.py` a little bit to accept `Base64 Encoded String` as the input.

```python  title="app.py" linenums="1" hl_lines="1-2 4 12-22"
import base64
from io import BytesIO

from PIL import Image
from transformers import pipeline

from pinferencia import Server, task

vision_classifier = pipeline(task="image-classification")


def classify(images: list) -> list:
    """Image Classification

    Args:
        images (list): list of base64 encoded image strings

    Returns:
        list: list of classification results
    """
    input_images = [Image.open(BytesIO(base64.b64decode(img))) for img in images]
    return vision_classifier(images=input_images)


service = Server()
service.register(
    model_name="vision",
    model=classify,
    metadata={"task": task.IMAGE_CLASSIFICATION},
)

```

## Predict Again

=== "UI"

    Open http://127.0.0.1:8501, and the template `Image Classification` will be selected automatically.

    ![UI](/assets/images/examples/huggingface/vision.jpg)

=== "Curl"

    ```bash
    curl --location --request POST 'http://127.0.0.1:8000/v1/models/vision/predict' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "data": "..."
    }'
    ```

    Result:
    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```

=== "Python requests"

    ```python title="test.py" linenums="1"
    import requests

    response = requests.post(
        url="http://localhost:8000/v1/models/vision/predict",
        json={
            "data": "..."  # noqa
        },
    )
    print("Prediction:", response.json()["data"])
    ```

    Run `python test.py` and result:

    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```
