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
pip install pinferencia streamlit
```

### 创建app.py

让我们将我们的预测函数保存到一个文件 `app.py` 中并添加一些行来注册它。

```python title="app.py" linenums="1"
from transformers import pipeline

from pinferencia import Server

bert = pipeline("fill-mask", model="bert-base-uncased")


service = Server()
service.register(model_name="bert", model=lambda text: bert(text))


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

更酷的是，访问 http://127.0.0.1:8501，您将拥有一个交互式UI。

您可以在那里发送预测请求！
