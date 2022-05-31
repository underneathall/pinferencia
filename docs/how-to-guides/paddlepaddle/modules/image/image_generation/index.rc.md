
## 模型基本信息

> 本模型封装自[小视科技 photo2cartoon 项目的 paddlepaddle 版本](https://github.com/minivision-ai/photo2cartoon-paddle)。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/Image_gan/style_transfer/Photo2Cartoon


### 样例结果示例

输入文件路径，模型将给出它的预测：

=== "输入"

图片来源 (https://www.pexels.com)

![人脸](/assets/images/examples/paddle/face.jpg)

=== "输出"

![人脸](/assets/images/examples/paddle/image_gen_output.jpg)

:fontawesome-regular-face-laugh-wink: 现在就来试试吧

## 先决条件

### 1、环境依赖  

请访问 [依赖项](/ml/paddlepaddle/dependencies/)

### 2、mobilenet_v2_animals 依赖  

  - paddlepaddle >= 2.0.0  

  - paddlehub >= 2.0.0


### 3、下载模型

```
hub install Photo2Cartoon
```

## 服务模型

### 安装 Pinferencia

首先，让我们安装 [Pinferencia](https://github.com/underneathall/pinferencia)。

```bash
pip install "pinferencia[uvicorn]"
```

### 创建app.py

让我们将我们的预测函数保存到一个文件 `app.py` 中并添加一些行来注册它。

```python title="app.py" linenums="1"
import base64
from io import BytesIO
from typing import Dict

import cv2
import paddlehub as hub
from PIL import Image

from pinferencia import Server, task
from pinferencia.tools import base64_str_to_cv2

image_generation = hub.Module(name="Photo2Cartoon")


def predict(data: Dict[str, str]):
    base64_img_str = data.get("base64_img_str")
    path = data.get("path")
    images = [cv2.imread(path)] if path else [base64_str_to_cv2(base64_img_str)]
    result = image_generation.Cartoon_GEN(images=images, visualization=True, output_dir="./")
    pil_img = Image.fromarray(result[0])
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


service = Server()
service.register(
    model_name="image_generation",
    model=predict,
    metadata={"task": task.URL_IMAGE_TO_IMAGE},
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

    打开http://127.0.0.1:8501，模板 `Url Image To Image` 会自动选中。

    ![png](/assets/images/examples/paddle/image_generation.jpg)

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/image_generation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": {"path": "test.jpg"}
        }'
    ```

    **响应**

    ```
    {
        "model_name": "image_generation",
        "model_version": "default",
        "data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a..."
    }
    ```

=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/image_generation/predict",
        headers = {"Content-type": "application/json"},
        json={"data": {"path": "test.jpg"}}
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

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

更酷的是，访问 http://127.0.0.1:8000，您将拥有一个完整的 API 文档。

您甚至也可以在那里发送预测请求！
