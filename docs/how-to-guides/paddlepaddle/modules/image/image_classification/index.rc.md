

## 模型基本信息

> MobileNet V2 是一个轻量化的卷积神经网络，它在 MobileNet 的基础上，做了 Inverted Residuals 和 Linear bottlenecks 这两大改进。该 PaddleHub Module 是在百度自建动物数据集上训练得到的，可用于图像分类和特征提取，当前已支持 7978 种动物的分类识别。模型的详情可参考[论文](https://arxiv.org/pdf/1801.04381.pdf)。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/face_detection/pyramidbox_lite_server


## 样本结果示例

输入文件路径，模型将给出它的预测：

=== "输入"

图片来源 (https://www.pexels.com)

![animal](/assets/images/examples/paddle/animal.jpg)

=== "输出"

`松鼠`

:fontawesome-regular-face-laugh-wink: 现在就来试试吧

## 先决条件

### 1、环境依赖

请访问 [依赖项](../../../dependencies/)

### 2、mobilenet_v2_animals 依赖

  - paddlepaddle >= 1.6.2

  - paddlehub >= 1.6.0


### 3、下载模型

```bash
hub install pyramidbox_lite_server
```

## 服务模型

### 安装 Pinferencia

首先，让我们安装 [Pinferencia](https://github.com/underneathall/pinferencia)。

```bash
pip install "pinferencia[streamlit]"
```

### 创建app.py

让我们将我们的预测函数保存到一个文件 `app.py` 中并添加一些行来注册它。

```python title="app.py" linenums="1"
import base64

import cv2
import numpy as np
import paddlehub as hub

from pinferencia import Server, task

classifier = hub.Module(name="mobilenet_v2_animals")


def base64_str_to_cv2(base64_str: str) -> np.ndarray:
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR
    )


def predict(data: list) -> list:
    images = [base64_str_to_cv2(base64_img_str) for base64_img_str in data]
    return classifier.classification(images=images)


service = Server()
service.register(
    model_name="classifier",
    model=predict,
    metadata={"task": task.IMAGE_TO_TEXT},
)


```

运行服务，等待它加载模型并启动服务器：

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

### 测试服务

!!! 提示

    图片存在于 service 机器上，可输入对于 service 文件的相对路径或者是文件的绝对路径

=== "UI"

    打开http://127.0.0.1:8501，模板 `Url Image To Text` 会自动选中。

    ![png](/assets/images/examples/paddle/image_classification.png)

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/classifier/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{"data": ["/9j/4AAQS........"]}'
    ```

    **响应**

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

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/classifier/predict",
        headers = {"Content-type": "application/json"},
        json={"data": ["/9j/4AAQS........"]},
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

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

更酷的是，访问 http://127.0.0.1:8000，您将拥有一个完整的 API 文档。

您甚至也可以在那里发送预测请求！
