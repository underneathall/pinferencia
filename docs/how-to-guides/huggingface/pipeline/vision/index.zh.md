
在本教程中，我们将探讨如何使用 Hugging Face 管道，以及如何使用 [Pinferencia](https://github.com/underneathall/pinferencia) 作为 REST API 部署它。

---


## 先决条件

请访问 [依赖项](/ml/huggingface/dependencies/)

## 下载模型并预测

模型将自动下载。

```python linenums="1"
from transformers import pipeline
vision_classifier = pipeline(task="image-classification")

vision_classifier(
    images="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"
)
```

![hfimg](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg)

结果:

```python
[{'label': 'lynx, catamount', 'score': 0.4403027892112732},
 {'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor',
  'score': 0.03433405980467796},
 {'label': 'snow leopard, ounce, Panthera uncia',
  'score': 0.032148055732250214},
 {'label': 'Egyptian cat', 'score': 0.02353910356760025},
 {'label': 'tiger cat', 'score': 0.023034192621707916}]
```

如此简单！ 现在让我们试试：

## 部署模型

没有部署，机器学习教程怎么可能完整？

首先，让我们安装 [Pinferencia](https://github.com/underneathall/pinferencia)。

```bash
pip install "pinferencia[streamlit]"
```

现在让我们用代码创建一个 `app.py` 文件：

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

容易，对吧？

## 预测

=== "Curl"

    ```bash
    curl --location --request POST 'http://127.0.0.1:8000/v1/models/vision/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"
        }'
    ```

    结果:
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

    运行 `python test.py` ，查看结果：

    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```

更酷的是，访问 http://127.0.0.1:8501，您将拥有一个交互式 ui。

您可以在那里发送预测请求！

## 进一步改进

但是，有时使用图像的 url 来预测是不合适的。

让我们稍微修改 `app.py` 以接受 `Base64 Encoded String` 作为输入。

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

## 再次预测

=== "UI"

    打开http://127.0.0.1:8501，会自动选择模板`图片分类`。

    ![UI](/assets/images/examples/huggingface/vision.jpg)

=== "Curl"

    ```bash
    curl --location --request POST 'http://127.0.0.1:8000/v1/models/vision/predict' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "data": "..."
    }'
    ```

    结果：

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

    运行 `python test.py` 并查看结果：

    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```
