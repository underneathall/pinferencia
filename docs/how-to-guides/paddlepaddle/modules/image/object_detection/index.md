
## Model basic information

> Vehicle detection is a very important and challenging task in urban traffic monitoring. The difficulty of this task lies in accurately localizing and classifying relatively small vehicles in complex scenes. The network of the PaddleHub Module is YOLOv3, of which the backbone is DarkNet53, which is trained by Baidu's self-built large-scale vehicle data set, and supports the recognition of car, truck, bus, motorbike, tricycle and other models.

Reference：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/image/object_detection/yolov3_darknet53_vehicles


## Sample result example

Enter the file path and the model will give its predictions：

=== "Input"

Image Source (https://www.pexels.com)

![car](/assets/images/examples/paddle/car_input.jpg)

=== "Output"

![car](/assets/images/examples/paddle/car_output.jpg)

:fontawesome-regular-face-laugh-wink: Let's try it out now

## Prerequisite

### 1、environment dependent  

Please visit [dependencies](/ml/paddlepaddle/dependencies/)

### 2、yolov3_darknet53_vehicles dependent  

  - paddlepaddle >= 1.6.2  

  - paddlehub >= 1.6.0

### 3、Download the model

```
hub install yolov3_darknet53_vehicles
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

Run the service, and wait for it to load the model and start the server:

<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Test the service

!!! tips

    The image exists on the service machine, you can enter the relative path of the service file or the absolute path of the file


=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/vehicle_detection/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "car.jpg"
        }'
    ```

    **Response**

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

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/vehicle_detection/predict",
        json={"data": "car.jpg"}
    )
    print(response.json())

    ```
    **Run the script and check the result.**

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
