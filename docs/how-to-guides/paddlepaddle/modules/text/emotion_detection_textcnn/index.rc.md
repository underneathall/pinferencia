

## 模型基本信息

> 对话情绪识别（Emotion Detection，简称 EmoTect）专注于识别智能对话场景中用户的情绪，针对智能对话场景中的用户文本，自动判断该文本的情绪类别并给出相应的置信度，情绪类型分为积极、消极、中性。该模型基于TextCNN（多卷积核 CNN 模型），能够更好地捕捉句子局部相关性。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/sentiment_analysis/emotion_detection_textcnn


## 样本结果示例

=== "输入"

    ```
    ["今天天气真好", "湿纸巾是干垃圾", "别来吵我"]
    ```

=== "输出"

    ```
    [
        {
            'text':'今天天气真好',
            'emotion_label':2,
            'emotion_key':'positive',
            'positive_probs':0.9267,
            'negative_probs':0.0019,
            'neutral_probs':0.0714
        },
        {
            'text':'湿纸巾是干垃圾',
            'emotion_label':1,
            'emotion_key':'neutral',
            'positive_probs':0.0062,
            'negative_probs':0.0042,
            'neutral_probs':0.9896
        },
        {
            'text':'别来吵我',
            'emotion_label':0,
            'emotion_key':'negative',
            'positive_probs':0.0732,
            'negative_probs':0.7791,
            'neutral_probs':0.1477
        }
    ]
    ```

:fontawesome-regular-face-laugh-wink: 现在就来试试吧


## 先决条件

### 1、环境依赖    

请访问 [依赖项](/ml/paddlepaddle/dependencies/)

### 2、emotion_detection_textcnn 依赖  

  - paddlepaddle >= 1.8.0 

  - paddlehub >= 1.8.0

### 3、下载模型

```
hub install emotion_detection_textcnn
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
import paddlehub as hub

from pinferencia import Server
emotion_detection_textcnn = hub.Module(name="emotion_detection_textcnn")


def predict(text: list):
    return emotion_detection_textcnn.emotion_classify(texts=text)


service = Server()
service.register(
    model_name="emotion_detection_textcnn",
    model=predict,
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

    打开http://127.0.0.1:8501，模板 `Raw Request` 会自动选中。

    ![png](/assets/images/examples/paddle/emotion_detection_textcnn.png)

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/emotion_detection_textcnn/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": ["今天天气真好", "湿纸巾是干垃圾", "别来吵我"]
        }'
    ```

    **响应**

    ```
    {
        "model_name": "emotion_detection_textcnn",
        "data": [
            {
                "text": "今天天气真好",
                "emotion_label": 2,
                "emotion_key": "positive",
                "positive_probs": 0.9267,
                "negative_probs": 0.0019,
                "neutral_probs": 0.0714
            },
            {
                "text": "湿纸巾是干垃圾",
                "emotion_label": 1,
                "emotion_key": "neutral",
                "positive_probs": 0.0062,
                "negative_probs": 0.0042,
                "neutral_probs": 0.9896
            },
            {
                "text": "别来吵我",
                "emotion_label": 0,
                "emotion_key": "negative",
                "positive_probs": 0.0732,
                "negative_probs": 0.7791,
                "neutral_probs": 0.1477
            }
        ]
    }
    ```


=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/emotion_detection_textcnn/predict",
        json={"data": ["今天天气真好", "湿纸巾是干垃圾", "别来吵我"]}
    )
    print(response.json())
    ```
    **运行脚本并检查结果。**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "emotion_detection_textcnn",
        "data": [
            {
                "text": "今天天气真好",
                "emotion_label": 2,
                "emotion_key": "positive",
                "positive_probs": 0.9267,
                "negative_probs": 0.0019,
                "neutral_probs": 0.0714
            },
            {
                "text": "湿纸巾是干垃圾",
                "emotion_label": 1,
                "emotion_key": "neutral",
                "positive_probs": 0.0062,
                "negative_probs": 0.0042,
                "neutral_probs": 0.9896
            },
            {
                "text": "别来吵我",
                "emotion_label": 0,
                "emotion_key": "negative",
                "positive_probs": 0.0732,
                "negative_probs": 0.7791,
                "neutral_probs": 0.1477
            }
        ]
    }
    ```

    </div>

---

更酷的是，访问 http://127.0.0.1:8501，您将拥有一个交互式UI。

您可以在那里发送预测请求！
