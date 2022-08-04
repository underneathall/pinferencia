

## 模型基本信息

> 该 Module 是 jieba 使用 PaddlePaddle 深度学习框架搭建的切词网络（双向 GRU）。同时也支持 jieba 的传统切词方法，如精确模式、全模式、搜索引擎模式等切词模式，使用方法和 jieba 保持一致。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/lexical_analysis/jieba_paddle


## 样本结果示例

=== "输入"

    ```
    "今天天气真好"
    ```
=== "输出"

    ```json
    ["今天", "天气", "真好"]
    ```

:fontawesome-regular-face-laugh-wink: 现在就来试试吧


## 先决条件

### 1、环境依赖

请访问 [依赖项](../../../dependencies/)

### 2、jieba_paddle 依赖

- paddlepaddle >= 1.8.0

- paddlehub >= 1.8.0

### 3、下载模型

```bash
hub install jieba_paddle
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

lexical_analysis = hub.Module(name="jieba_paddle")


def predict(text: str):
    return lexical_analysis.cut(text, cut_all=False, HMM=True)


service = Server()
service.register(
    model_name="lexical_analysis", model=predict, metadata={"task": task.TEXT_TO_TEXT}
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

    打开http://127.0.0.1:8501，模板 `Text to Text` 会自动选中。

    ![png](/assets/images/examples/paddle/lexical.jpg)

=== "curl"

    **请求**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/lexical_analysis/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "今天天气真好"
        }'
    ```

    **响应**

    ```
    {
        "model_name": "lexical_analysis",
        "data": [
            "今天",
            "天气",
            "真好"
        ]
    }
    ```


=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/lexical_analysis/predict",
        json={"data": "今天天气真好"}
    )
    print(response.json())
    ```
    **运行脚本并检查结果。**

    <div class="termy">

    ```console
    $ python test.py
    {
        "model_name": "lexical_analysis",
        "data": [
            "今天",
            "天气",
            "真好"
        ]
    }
    ```

    </div>

---

更酷的是，访问 http://127.0.0.1:8501，您将拥有一个交互式UI。

您可以在那里发送预测请求！
