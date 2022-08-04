

## 模型基本信息

> ERNIE-GEN 是面向生成任务的预训练-微调框架，首次在预训练阶段加入 span-by-span 生成任务，让模型每次能够生成一个语义完整的片段。在预训练和微调中通过填充式生成机制和噪声感知机制来缓解曝光偏差问题。此外, ERNIE-GEN 采样多片段-多粒度目标文本采样策略, 增强源文本和目标文本的关联性，加强了编码器和解码器的交互。ernie_gen_poetry 采用开源诗歌数据集进行微调，可用于生成诗歌。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/text_generation/ernie_gen_poetry


## 样本结果示例

=== "输入"

    ```json
    ["昔年旅南服，始识王荆州。", "高名出汉阴，禅阁跨香岑。"]
    ```
=== "输出"

    ```json
    [
        [
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，俯仰成春秋。",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与夫子，相逢",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与君别，飘零",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，各在",
            "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，风雨"
        ],
        [
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树林。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树阴。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂林。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏正森。",
            "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂阴。"
        ]
    ]
    ```

:fontawesome-regular-face-laugh-wink: 现在就来试试吧


## 先决条件

### 1、环境依赖

请访问 [依赖项](../../../dependencies/)

### 2、ernie_gen_poetry 依赖

- paddlepaddle >= 2.0.0

- paddlehub >= 2.0.0

- paddlenlp >= 2.0.0

```bash
pip3 install paddlenlp
```

### 3、下载模型

```bash
hub install ernie_gen_poetry
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
import paddlehub as hub

from pinferencia import Server, task

text_generation = hub.Module(name="ernie_gen_poetry")


def predict(texts: list) -> list:
    return text_generation.generate(texts=texts, beam_width=5)


service = Server()
service.register(
    model_name="text_generation",
    model=predict,
    metadata={"task": task.TEXT_TO_TEXT},
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

    打开http://127.0.0.1:8501，模板 `TEXT_TO_TEXT` 会自动选中。

    ![png](/assets/images/examples/paddle/text_gen.jpg)

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/text_generation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": ["昔年旅南服，始识王荆州。", "高名出汉阴，禅阁跨香岑。"]
        }'
    ```

    **响应**

    ```
    {
        "model_name": "text_generation",
        "data": [
            [
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，俯仰成春秋。",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与夫子，相逢",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与君别，飘零",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，各在",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，风雨"
            ],
            [
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树阴。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏正森。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂阴。"
            ]
        ]
    }
    ```


=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/text_generation/predict",
        json={"data": ["昔年旅南服，始识王荆州。", "高名出汉阴，禅阁跨香岑。"]}
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "text_generation",
        "data": [
            [
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，俯仰成春秋。",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与夫子，相逢",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况我与君别，飘零",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，各在",
                "一见便倾盖，论交更绸缪。别来二十年，日月如奔流。人生会合难，况乃岁月遒。君家富文史，我老无田畴。相逢不相识，各在天一陬。人生百年内，聚散如浮沤。况复各异乡，风雨"
            ],
            [
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏树阴。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂林。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前柏正森。",
                "地僻无尘到，山高见水深。钟声传远寺，塔影落前林。欲问西来意，庭前有桂阴。"
            ]
        ]
    }
    ```

    </div>

---

更酷的是，访问 http://127.0.0.1:8501，您将拥有一个交互式UI。

您可以在那里发送预测请求！
