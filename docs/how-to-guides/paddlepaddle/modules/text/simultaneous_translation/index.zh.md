

## 模型基本信息

> 同声传译（Simultaneous Translation），即在句子完成之前进行翻译，同声传译的目标是实现同声传译的自动化，它可以与源语言同时翻译，延迟时间只有几秒钟。

参考：https://github.com/PaddlePaddle/PaddleHub/blob/release/v2.2/modules/text/simultaneous_translation/stacl/transformer_nist_wait_1


## 样本结果示例

输入文件路径，模型将给出它的预测：

=== "输入"

    ```
    [
        "他",
        "他还",
        "他还说",
        "他还说现在",
        "他还说现在正在",
        "他还说现在正在为",
        "他还说现在正在为这",
        "他还说现在正在为这一",
        "他还说现在正在为这一会议",
        "他还说现在正在为这一会议作出",
        "他还说现在正在为这一会议作出安排",
        "他还说现在正在为这一会议作出安排。",
    ]
    ```
=== "输出"

    ```
    input: 他
    model output: he

    input: 他还
    model output: he also

    input: 他还说
    model output: he also said

    input: 他还说现在
    model output: he also said that

    input: 他还说现在正在
    model output: he also said that he

    input: 他还说现在正在为
    model output: he also said that he is

    input: 他还说现在正在为这
    model output: he also said that he is making

    input: 他还说现在正在为这一
    model output: he also said that he is making preparations

    input: 他还说现在正在为这一会议
    model output: he also said that he is making preparations for

    input: 他还说现在正在为这一会议作出
    model output: he also said that he is making preparations for this

    input: 他还说现在正在为这一会议作出安排
    model output: he also said that he is making preparations for this meeting

    input: 他还说现在正在为这一会议作出安排。
    model output: he also said that he is making preparations for this meeting .
    ```

:fontawesome-regular-face-laugh-wink: 现在就来试试吧


## 先决条件

### 1、环境依赖

请访问 [依赖项](../../../dependencies/)

### 2、transformer_nist_wait_1 依赖

  - paddlepaddle >= 2.1.0

  - paddlehub >= 2.1.0

### 3、下载模型

```bash
hub install transformer_nist_wait_1
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

from pinferencia import Server

simultaneous_translation = hub.Module(name="transformer_nist_wait_1")


def predict(text: list):
    for t in text:
        print(f"input: {t}")
        result = simultaneous_translation.translate(t)
        print(f"model output: {result}")


service = Server()
service.register(model_name="simultaneous_translation", model=predict)

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
        'http://127.0.0.1:8000/v1/models/simultaneous_translation/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": [
                "他",
                "他还",
                "他还说",
                "他还说现在",
                "他还说现在正在",
                "他还说现在正在为",
                "他还说现在正在为这",
                "他还说现在正在为这一",
                "他还说现在正在为这一会议",
                "他还说现在正在为这一会议作出",
                "他还说现在正在为这一会议作出安排",
                "他还说现在正在为这一会议作出安排。",
            ]
        }'
    ```

    **响应**

    在server页面
    ```
    input: 他
    model output: he

    input: 他还
    model output: he also

    input: 他还说
    model output: he also said

    input: 他还说现在
    model output: he also said that

    input: 他还说现在正在
    model output: he also said that he

    input: 他还说现在正在为
    model output: he also said that he is

    input: 他还说现在正在为这
    model output: he also said that he is making

    input: 他还说现在正在为这一
    model output: he also said that he is making preparations

    input: 他还说现在正在为这一会议
    model output: he also said that he is making preparations for

    input: 他还说现在正在为这一会议作出
    model output: he also said that he is making preparations for this

    input: 他还说现在正在为这一会议作出安排
    model output: he also said that he is making preparations for this meeting

    input: 他还说现在正在为这一会议作出安排。
    model output: he also said that he is making preparations for this meeting .
    ```


=== "Python Requests"

    **创建`test.py`。**

    ```python title="test.py" linenums="1"
    import requests


    requests.post(
        url="http://localhost:8000/v1/models/simultaneous_translation/predict",
        json={"data": [
                "他",
                "他还",
                "他还说",
                "他还说现在",
                "他还说现在正在",
                "他还说现在正在为",
                "他还说现在正在为这",
                "他还说现在正在为这一",
                "他还说现在正在为这一会议",
                "他还说现在正在为这一会议作出",
                "他还说现在正在为这一会议作出安排",
                "他还说现在正在为这一会议作出安排。",
            ]}
    )
    ```
    **运行脚本并检查结果。**

    <div class="termy">

    ```console
    $ python test.py
    # 在server页面
    input: 他
    model output: he

    input: 他还
    model output: he also

    input: 他还说
    model output: he also said

    input: 他还说现在
    model output: he also said that

    input: 他还说现在正在
    model output: he also said that he

    input: 他还说现在正在为
    model output: he also said that he is

    input: 他还说现在正在为这
    model output: he also said that he is making

    input: 他还说现在正在为这一
    model output: he also said that he is making preparations

    input: 他还说现在正在为这一会议
    model output: he also said that he is making preparations for

    input: 他还说现在正在为这一会议作出
    model output: he also said that he is making preparations for this

    input: 他还说现在正在为这一会议作出安排
    model output: he also said that he is making preparations for this meeting

    input: 他还说现在正在为这一会议作出安排。
    model output: he also said that he is making preparations for this meeting .
    ```

    </div>

---
