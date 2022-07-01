# 自定义前端信息

**Pinferencia** 前端支持自定义：

- 网页的标题
- 使用模型 `display_name` 作为模板的标题
- 简短的介绍
- 和详细说明

## 首先让我们创建一个简单的模型服务

```python title="app.py" linenums="1"
from typing import List

from pinferencia import Server


def stat(data: List[float]) -> float:
    return sum(data)


service = Server()
service.register(
    model_name="stat",
    model=stat,
    metadata={"display_name": "Awesome Model"}, # (1)
)

```

1. 这将更改右侧内容区域显示的默认模板标题。

现在启动服务：

<div class="termy">

```console
$ pinfer app:service

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

你会得到：

![display name](/assets/images/examples/custom-frontend-display-name.jpg)

## 自定义前端

```python title="app.py" linenums="1"
from pinferencia.frontend.app import Server

detail_description = """
# My Awesome Model

This is the service of my awesome model.

It is **fast**, **simple**, and **beautiful**.

Visit [My Awesome Model Home](/abc) to learn more about it.
"""

service = Server(
    title="My Awesome Model", # (1)
    short_description="This is the short description", # (2)
    detail_description=detail_description, # (3)
    backend_server="http://127.0.0.1:8000",
)

```

1. 这将改变左侧面板顶部显示的标题。
2. 这将更改左侧面板标题下方的描述。
3. 这将改变页面的关于信息。

现在启动服务：

<div class="termy">

```console
$ pinfer app:service --frontend-script=frontend.py

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

你会得到：

![display name](/assets/images/examples/custom-frontend.jpg)
