
## 模型基本信息
> chinese_ocr_db_crnn_mobile Module 用于识别图片当中的汉字, 识别文本框中的中文文字,再对检测文本框进行角度分类。最终识别文字算法采用 CRNN（Convolutional Recurrent Neural Network）即卷积递归神经网络。该 Module 是一个超轻量级中文 OCR 模型，支持直接预测。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/text_recognition/chinese_ocr_db_crnn_mobile

## 模型是如何工作的？

输入文件路径，模型将给出它的预测：

=== "输入"

图片来源 (https://www.pexels.com)

![价格](/assets/images/examples/paddle/price_input.jpg)

=== "输出"

![价格](/assets/images/examples/paddle/price_output.jpg)

:fontawesome-regular-face-laugh-wink: 现在就来试试吧

## 先决条件

### 1、环境依赖

请访问 [依赖项](../../../dependencies/)

### 2、mobilenet_v2_animals 依赖

  - paddlepaddle >= 1.6.2

  - paddlehub >= 1.6.0

```
pip3 install shapely pyclipper
```

### 3、下载模型

```bash
hub install chinese_ocr_db_crnn_mobile
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
from pinferencia import Server

import paddlehub as hub
import cv2

ocr = hub.Module(
    name="chinese_ocr_db_crnn_mobile", enable_mkldnn=True
)  # mkldnn加速仅在CPU下有效


def predict(path: str):
    return ocr.recognize_text(
        images=[cv2.imread(path)],
        visualization=True,
        output_dir="./"
    )


service = Server()
service.register(model_name="ocr", model=predict)

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
        'http://127.0.0.1:8000/v1/models/ocr/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "test.jpg"
        }'
    ```

    **响应**

    ```
    {'model_name': 'text_gencognition', 'model_version': 'default', 'data': [{'save_path': './ndarray_1655277391.4650576.jpg', 'data': [{'text': 'photo', 'confidence': 0.9524916410446167, 'text_box_position': [[1145, 1913], [1243, 1913], [1243, 1934], [1145, 1934]]}, {'text': 'AARON TUAN', 'confidence': 0.9474555850028992, 'text_box_position': [[1236, 1909], [1424, 1909], [1424, 1937], [1236, 1937]]}, {'text': '#makeup ANNA LE', 'confidence': 0.8719193339347839, 'text_box_position': [[1168, 1934], [1424, 1930], [1424, 1960], [1168, 1964]]}, {'text': '#ekip MT RYDER', 'confidence': 0.9155644178390503, 'text_box_position': [[1193, 1962], [1421, 1962], [1421, 1984], [1193, 1984]]}]}]}
    ```

=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/ocr/predict",
        json={"data": "test.jpg"}
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

    <div class="termy">

    ```console
    $ python test.py
    {'model_name': 'text_gencognition', 'model_version': 'default', 'data': [{'save_path': './ndarray_1655277391.4650576.jpg', 'data': [{'text': 'photo', 'confidence': 0.9524916410446167, 'text_box_position': [[1145, 1913], [1243, 1913], [1243, 1934], [1145, 1934]]}, {'text': 'AARON TUAN', 'confidence': 0.9474555850028992, 'text_box_position': [[1236, 1909], [1424, 1909], [1424, 1937], [1236, 1937]]}, {'text': '#makeup ANNA LE', 'confidence': 0.8719193339347839, 'text_box_position': [[1168, 1934], [1424, 1930], [1424, 1960], [1168, 1964]]}, {'text': '#ekip MT RYDER', 'confidence': 0.9155644178390503, 'text_box_position': [[1193, 1962], [1421, 1962], [1421, 1984], [1193, 1984]]}]}]}
    ```

    </div>

---
