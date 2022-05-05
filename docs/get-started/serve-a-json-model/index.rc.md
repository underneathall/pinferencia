# 启动一个 JSON 模型

现在先让我们尝试一个简单的例子，让你来熟悉 **Pinferecia**.

!!! info "太长不看"

    熟悉如何通过 **Pinferencia** 注册和上线一个模型非常重要。

    不过，如果你想现在就尝试机器学习模型，你可以移步[启动 Pytorch MNIST Model](../pytorch-mnist)

## 定义 JSON 模型

让我们先创建一个文件 `app.py`.

下面就是这个 JSON 模型.

输入是`a`返回`1`,  输入`b`返回`2`, 其他输入返回`0`。

```python title="app.py" linenums="1"
class JSONModel:
    def predict(self, data):
        knowledge = {"a": 1, "b": 2}
        return knowledge.get(data, 0)

```

## 创建服务并注册模型

首先从 `pinferencia` 导入 `Server` , 然后创建一个server实例并注册 `JSON 模型`.

```python title="app.py" linenums="1" hl_lines="1 10 11 12"
from pinferencia import Server


class JSONModel:
    def predict(self, data: str) -> int:
        knowledge = {"a": 1, "b": 2}
        return knowledge.get(data, 0)


model = JSONModel()
service = Server()
service.register(model_name="json", model=model, entrypoint="predict")

```

!!! tip "model_name 和 entrypoint 是什么意思?"
    **model_name** 你给这个模型取的名字。
    这里我们取名 `json`, 对应的这个模型的地址就是 `http://127.0.0.1:8000/v1/models/json`.

    如果关于API你有什么不清楚的，你可以随时访问下面将要提到的在线API文档页面。


    **entrypoint** `predict` 意味着我们会使用 `JSON 模型` 的 `predict`函数来预测数据。

## 启动服务

<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

打开浏览器访问 **http://127.0.0.1:8000**, 现在你拥有了一个自动生成的 API 文档页面!

!!! info "FastAPI and Starlette"
    **Pinferencia** 基于 [FastAPI](https://fastapi.tiangolo.com)，其又基于 [Starlette](https://www.starlette.io).

    多亏了他们，您将拥有一个带有 OpenAPI 规范的 API。这意味着您将拥有一个自动文档网页，并且客户端代码也可以自动生成。

!!! tips "提示"
    **Pinferencia** 提供了两个 API 文档地址:

    - http://127.0.0.1:8000 or http://127.0.0.1:8000/docs
    - http://127.0.0.1:8000/redoc

您可以查看 API 规范，甚至可以自己 **试用** API！

![Swagger UI](/assets/images/swagger-ui.jpg)

## 测试 API

**使用下面的代码创建一个`test.py`。**

!!! tips "提示"
    你需要安装 `requests`.
    ```bash
    pip install requests
    ```

```python title="test.py" linenums="1"
import requests


response = requests.post(
    url="http://localhost:8000/v1/models/json/predict",
    json={"data": "a"},
)
print(response.json())

```

**运行脚本并检查结果.**

<div class="termy">

```console
$ python test.py
{'model_name': 'json', 'data': 1}
```

</div>

**现在让我们再添加两个输入，并让打印更漂亮.**

```python title="test.py" linenums="1" hl_lines="3-6 9-11"
import requests

print("|{:^10}|{:^15}|".format("Input", "Prediction"))
print("|{:^10}|{:^15}|".format("-" * 10, "-" * 15))

for character in ["a", "b", "c"]:
    response = requests.post(
        url="http://localhost:8000/v1/models/json/predict",
        json={"data": character},
    )
    print(f"|{character:^10}|{str(response.json()['data']):^15}|")

```

**再次运行脚本并检查结果。**

<div class="termy">

```console
$ python test.py
|  Input   |  Prediction   |
|----------|---------------|
|    a     |       1       |
|    b     |       2       |
|    c     |       0       |
```

</div>