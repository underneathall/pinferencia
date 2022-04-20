# Google T5 翻译即服务，只需 7 行代码

什么是T5？ Google 的 Text-To-Text Transfer Transformer (T5) 提供了翻译功能。

![翻译](/asserts/images/examples/translate-home.png)

在本文中，我们将 Google T5 模型部署为 REST API 服务。 难的？ 我告诉你怎么样：你只需要写 7 行代码？

![翻译](/asserts/images/examples/translate-app.png)

## 安装依赖

### HuggingFace

```bash
pip install "transformers[pytorch]"
```

如果不起作用，请访问 [Installation](https://huggingface.co/docs/transformers/installation) 并查看其官方文档。

### Pinferencia

```bash
pip install "pinferencia[uvicorn]"
```

## 定义服务

首先让我们创建 app.py 来定义服务：

```python title="app.py" linenums="1"
from transformers import pipeline

from pinferencia import Server

t5 = pipeline(model="t5-base", tokenizer="t5-base")


def translate(text):
    return t5(text)


service = Server()
service.register(model_name="t5", model=translate)
```

##启动服务

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

=== "Curl"

    ```bash
    curl -X 'POST' \
        'http://localhost:8000/v1/models/t5/predict' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "parameters": {},
        "data": "translate English to German: Good morning, my love."
    }'
    ```

    结果:
    
    ```json
    {
        "model_name": "t5",
        "data": [
            {
            "translation_text": "Guten Morgen, liebe Liebe."
            }
        ]
    }
    ```

=== "Python requests"

    ```python title="test.py" linenums="1"
    import requests

    response = requests.post(
        url="http://localhost:8000/v1/models/gpt2/predict",
        json={
            "data": "translate English to German: Good morning, my love."
        },
    )
    print("Prediction:", response.json()["data"])
    ```

    运行`python test.py`并打印结果：

    ```
    Prediction: {
        "translation_text": "Guten Morgen, liebe Liebe."
    }
    ```

---

更酷的是，访问 http://127.0.0.1:8000，您将拥有一个交互式 ui。

您可以在那里发送预测请求！
