
## 模型基本信息

> 基于 ExtremeC3 模型实现的轻量化人像分割模型, 更多详情请参考： [ExtremeC3_Portrait_Segmentation](https://github.com/clovaai/ext_portrait_segmentation) 项目。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/semantic_segmentation/ExtremeC3_Portrait_Segmentation

### 样例结果示例

=== "输入"

    ![image](/assets/images/examples/paddle/seg.jpg)

=== "输出"

    ![image](/assets/images/examples/paddle/seg_0.png)

    ![image](/assets/images/examples/paddle/seg_mask_0.png)

:fontawesome-regular-face-laugh-wink: 现在就来试试吧

## 先决条件

### 1、环境依赖

请访问 [依赖项](../../../dependencies/)

### 2、ExtremeC3_Portrait_Segmentation 依赖

  - paddlepaddle >= 2.0.0

  - paddlehub >= 2.0.0

### 3、下载模型

```bash
hub install ExtremeC3_Portrait_Segmentation
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
from io import BytesIO

import cv2
import numpy as np
import paddlehub as hub
from PIL import Image

from pinferencia import Server, task

semantic_segmentation = hub.Module(name="ExtremeC3_Portrait_Segmentation")


def base64_str_to_cv2(base64_str: str) -> np.ndarray:
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_str), np.uint8), cv2.IMREAD_COLOR
    )


def predict(base64_img_str: str) -> str:
    images = [base64_str_to_cv2(base64_img_str)]
    result = semantic_segmentation.Segmentation(
        images=images,
        output_dir="./",
        visualization=True,
    )
    pil_img = Image.fromarray(result[0]["result"])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="semantic_segmentation",
    model=predict,
    metadata={"task": task.IMAGE_TO_IMAGE},
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

=== "UI"

    打开http://127.0.0.1:8501，模板 `Url Image To Image` 会自动选中。

    ![png](/assets/images/examples/paddle/semantic_segmentation.png)

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/semantic_segmentation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "/9j/4AAQSkZJRgABAQEA/..."
        }'
    ```

    **响应**

    ```
    {
        "model_name": "semantic_segmentation",
        "model_version": "default",
        "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRo..."
    }
    ```

=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/semantic_segmentation/predict",
        headers = {"Content-type": "application/json"},
        json={"data": "/9j/4AAQSkZJRgABAQEA/..."},
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

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

更酷的是，访问 http://127.0.0.1:8000，您将拥有一个完整的 API 文档。

您甚至也可以在那里发送预测请求！
