
## 模型基本信息

> 车辆检测是城市交通监控中非常重要并且具有挑战性的任务，该任务的难度在于对复杂场景中相对较小的车辆进行精准地定位和分类。该 PaddleHub Module 的网络为 YOLOv3, 其中 backbone 为 DarkNet53，采用百度自建大规模车辆数据集训练得到，支持 car (汽车)、truck (卡车)、bus (公交车)、motorbike (摩托车)、tricycle (三轮车)等车型的识别。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/object_detection/yolov3_darknet53_vehicles


## 样本结果示例

输入文件路径，模型将给出它的预测：

=== "输入"

图片来源 (https://www.pexels.com)

![车流](/assets/images/examples/paddle/car_input.jpg)

=== "输出"

![车流](/assets/images/examples/paddle/car_output.jpg)

:fontawesome-regular-face-laugh-wink: 现在就来试试吧

## 先决条件

### 1、环境依赖  

请访问 [依赖项](/ml/paddlepaddle/dependencies/)

### 2、yolov3_darknet53_vehicles 依赖  

  - paddlepaddle >= 1.6.2  

  - paddlehub >= 1.6.0

### 3、下载模型

```
hub install yolov3_darknet53_vehicles
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

vehicle_detection = hub.Module(name="yolov3_darknet53_vehicles")


def predict(path: str):
    return vehicle_detection.object_detection(
        images=[cv2.imread(path)], visualization=True, output_dir="./"
    )


service = Server()
service.register(model_name="vehicle_detection", model=predict)

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
        'http://127.0.0.1:8000/v1/models/vehicle_detection/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "car.jpg"
        }'
    ```

    **响应**

    ```
    {
        "model_name": "vehicle_detection",
        "data": [
            {
                "data": [
                    {
                        "label": "car",
                        "confidence": 0.9332570433616638,
                        "left": 832.1240234375,
                        "top": 1694.6256103515625,
                        "right": 1209.645263671875,
                        "bottom": 1972.4195556640625
                    },
                    {
                        "label": "car",
                        "confidence": 0.8977782130241394,
                        "left": 1476.706787109375,
                        "top": 1803.521240234375,
                        "right": 1796.732177734375,
                        "bottom": 2107.582275390625
                    },
                    {
                        "label": "car",
                        "confidence": 0.849329948425293,
                        "left": 1319.199462890625,
                        "top": 1679.5538330078125,
                        "right": 1513.8466796875,
                        "bottom": 1851.3421630859375
                    },
                    {
                        "label": "car",
                        "confidence": 0.8382290005683899,
                        "left": 1665.3941650390625,
                        "top": 1754.3929443359375,
                        "right": 2237.92138671875,
                        "bottom": 2323.58642578125
                    },
                    {
                        "label": "car",
                        "confidence": 0.8308005332946777,
                        "left": 2576.8466796875,
                        "top": 1775.929931640625,
                        "right": 4473.15087890625,
                        "bottom": 3095.475830078125
                    },
                    {
                        "label": "car",
                        "confidence": 0.6374166011810303,
                        "left": 2269.047119140625,
                        "top": 1852.68994140625,
                        "right": 3090.314208984375,
                        "bottom": 2686.0478515625
                    },
                    {
                        "label": "car",
                        "confidence": 0.5584644079208374,
                        "left": 1963.8443603515625,
                        "top": 1830.8948974609375,
                        "right": 2598.80126953125,
                        "bottom": 2392.88818359375
                    },
                    {
                        "label": "car",
                        "confidence": 0.28342998027801514,
                        "left": 1141.4927978515625,
                        "top": 1578.66015625,
                        "right": 1272.1849365234375,
                        "bottom": 1657.116455078125
                    },
                    {
                        "label": "car",
                        "confidence": 0.23879402875900269,
                        "left": 1186.671142578125,
                        "top": 1590.04052734375,
                        "right": 1316.980712890625,
                        "bottom": 1683.19970703125
                    },
                    {
                        "label": "carplate",
                        "confidence": 0.9311351776123047,
                        "left": 3628.1376953125,
                        "top": 2832.224853515625,
                        "right": 3963.41162109375,
                        "bottom": 2924.886962890625
                    },
                    {
                        "label": "carplate",
                        "confidence": 0.3726407289505005,
                        "left": 1056.91015625,
                        "top": 1856.930908203125,
                        "right": 1110.511962890625,
                        "bottom": 1878.08935546875
                    }
                ],
                "save_path": "./image_numpy_0.jpg"
            }
        ]
    }
    ```

=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/vehicle_detection/predict",
        json={"data": "car.jpg"}
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "vehicle_detection",
        "data": [
            {
                "data": [
                    {
                        "label": "car",
                        "confidence": 0.9332570433616638,
                        "left": 832.1240234375,
                        "top": 1694.6256103515625,
                        "right": 1209.645263671875,
                        "bottom": 1972.4195556640625
                    },
                    {
                        "label": "car",
                        "confidence": 0.8977782130241394,
                        "left": 1476.706787109375,
                        "top": 1803.521240234375,
                        "right": 1796.732177734375,
                        "bottom": 2107.582275390625
                    },
                    {
                        "label": "car",
                        "confidence": 0.849329948425293,
                        "left": 1319.199462890625,
                        "top": 1679.5538330078125,
                        "right": 1513.8466796875,
                        "bottom": 1851.3421630859375
                    },
                    {
                        "label": "car",
                        "confidence": 0.8382290005683899,
                        "left": 1665.3941650390625,
                        "top": 1754.3929443359375,
                        "right": 2237.92138671875,
                        "bottom": 2323.58642578125
                    },
                    {
                        "label": "car",
                        "confidence": 0.8308005332946777,
                        "left": 2576.8466796875,
                        "top": 1775.929931640625,
                        "right": 4473.15087890625,
                        "bottom": 3095.475830078125
                    },
                    {
                        "label": "car",
                        "confidence": 0.6374166011810303,
                        "left": 2269.047119140625,
                        "top": 1852.68994140625,
                        "right": 3090.314208984375,
                        "bottom": 2686.0478515625
                    },
                    {
                        "label": "car",
                        "confidence": 0.5584644079208374,
                        "left": 1963.8443603515625,
                        "top": 1830.8948974609375,
                        "right": 2598.80126953125,
                        "bottom": 2392.88818359375
                    },
                    {
                        "label": "car",
                        "confidence": 0.28342998027801514,
                        "left": 1141.4927978515625,
                        "top": 1578.66015625,
                        "right": 1272.1849365234375,
                        "bottom": 1657.116455078125
                    },
                    {
                        "label": "car",
                        "confidence": 0.23879402875900269,
                        "left": 1186.671142578125,
                        "top": 1590.04052734375,
                        "right": 1316.980712890625,
                        "bottom": 1683.19970703125
                    },
                    {
                        "label": "carplate",
                        "confidence": 0.9311351776123047,
                        "left": 3628.1376953125,
                        "top": 2832.224853515625,
                        "right": 3963.41162109375,
                        "bottom": 2924.886962890625
                    },
                    {
                        "label": "carplate",
                        "confidence": 0.3726407289505005,
                        "left": 1056.91015625,
                        "top": 1856.930908203125,
                        "right": 1110.511962890625,
                        "bottom": 1878.08935546875
                    }
                ],
                "save_path": "./image_numpy_0.jpg"
            }
        ]
    }
    ```

    </div>

---
