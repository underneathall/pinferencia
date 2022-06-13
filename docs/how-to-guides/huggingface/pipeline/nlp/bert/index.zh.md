你们中的许多人一定听说过“Bert”或“transformers”。
你可能还知道huggingface。

在本教程中，让我们使用它的 pytorch 转换器模型并通过 REST API 为它提供服务

## 模型是如何工作的？

输入一个不完整的句子，模型将给出它的预测：

=== "输入"

    ```
    Paris is the [MASK] of France.
    ```

=== "输出"

    ```
    Paris is the capital of France.
    ```

:fontawesome-regular-face-laugh-wink: 现在就来试试吧

## 先决条件

请访问 [依赖项](/ml/huggingface/dependencies/)

## 服务模型

### 安装 Pinferencia

首先，让我们安装 [Pinferencia](https://github.com/underneathall/pinferencia)。

```bash
pip install "pinferencia[streamlit]"
```

### 创建app.py

让我们将我们的预测函数保存到一个文件 `app.py` 中并添加一些行来注册它。

```python title="app.py" linenums="1"
from transformers import pipeline

from pinferencia import Server, task

bert = pipeline("fill-mask", model="bert-base-uncased")


def predict(text: str) -> list:
    return bert(text)


service = Server()
service.register(
    model_name="bert",
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

    打开http://127.0.0.1:8501，模板`Text to Text`会自动选中。

    ![UI](/assets/images/examples/huggingface/bert.jpg)

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/bert/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "Paris is the [MASK] of France."
        }'
    ```

    **响应**

    ```
    {
        "model_name":"bert",
        "data":"Paris is the capital of France."
    }
    ```

=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/bert/predict",
        json={"data": "Paris is the [MASK] of France."},
    )
    print(response.json())

    ```
    **运行脚本并检查结果。**

    <div class="termy">

    ```console
    $ python test.py
    {'model_name': 'bert', 'data': 'Paris is the capital of France.'}
    ```

    </div>

---

更酷的是，访问 http://127.0.0.1:8000，您将拥有一个完整的 API 文档。

您甚至也可以在那里发送预测请求！
