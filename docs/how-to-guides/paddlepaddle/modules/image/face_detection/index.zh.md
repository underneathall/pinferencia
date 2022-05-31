
## 模型基本信息

> PyramidBox-Lite 是基于 2018 年百度发表于计算机视觉顶级会议 ECCV 2018 的论文 PyramidBox 而研发的轻量级模型，模型基于主干网络 FaceBoxes，对于光照、口罩遮挡、表情变化、尺度变化等常见问题具有很强的鲁棒性。该 PaddleHub Module 基于 WIDER FACE 数据集和百度自采人脸数据集进行训练，支持预测，可用于人脸检测。

参考：https://github.com/PaddlePaddle/PaddleHub/tree/release/v2.2/modules/image/face_detection/pyramidbox_lite_server


## 样本结果示例

输入文件路径，模型将给出它的预测：

=== "输入"

图片来源 (https://www.pexels.com)

![人脸](/assets/images/examples/paddle/face.jpg)

=== "输出"

![人脸](/assets/images/examples/paddle/face_detector.jpg)

:fontawesome-regular-face-laugh-wink: 现在就来试试吧


## 先决条件

### 1、环境依赖  

请访问 [依赖项](/ml/paddlepaddle/dependencies/)

### 2、pyramidbox_lite_server 依赖  

  - paddlepaddle >= 1.6.2  

  - paddlehub >= 1.6.0


### 3、下载模型

```
hub install pyramidbox_lite_server
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
from pinferencia import Server

import paddlehub as hub
import cv2

face_detector = hub.Module(name="pyramidbox_lite_server")


def predict(path: str):
    return face_detector.face_detection(
        images=[cv2.imread(path)], visualization=True, output_dir="./"
    )


service = Server()
service.register(model_name="face_detector", model=predict)

```

运行服务，等待它加载模型并启动服务器：
<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>


### 测试服务

!!! 提示

    图片存在于 service 机器上，可输入对于 service 文件的相对路径或者是文件的绝对路径

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/face_detector/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "face.jpg"
        }'
    ```

    **响应**

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

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/face_detector/predict",
        headers = {"Content-type": "application/json"},
        json={"data": "face.jpg"}
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

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
