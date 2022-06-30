# 自定义模板

尽管有内置模板，但它永远不足以涵盖所有场景。

**Pinferencia** 支持自定义模板。自定义模板并在您的服务中使用它很容易。

首先让我们尝试创建一个简单的模板：

1. 输入数字列表。
2. 显示数字的平均值、最大值和最小值。

## 模型

模型很简单，服务可以定义为：

```python title="app.py" linenums="1"
from typing import List

from pinferencia import Server


def stat(data: List[float]) -> dict:
    return {
        "mean": sum(data) / len(data),
        "max": max(data),
        "min": min(data),
    }


service = Server()
service.register(model_name="stat", model=stat, metadata={"task": "Stat"})
```

## 模板

**Pinferencia** 提供了 `BaseTemplate` 来扩展以构建自定义模板。

### JSON 输入

首先，我们将页面分为两列，并分别创建一个 JSON 输入字段和显示字段。

```python title="frontend.py" linenums="1"
import streamlit as st

from pinferencia.frontend.app import Server
from pinferencia.frontend.templates.base import BaseTemplate


class StatTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Numbers</span> '
        '<span style="color:slategray;">Statistics</span>'
    )

    def render(self):
        super().render()
        json_template = "[]"
        col1, col2 = st.columns(2)
        col2.write("Request Preview")
        raw_text = col1.text_area("Raw Data", value=json_template, height=150)
        col2.json(raw_text)


backend_address = "http://127.0.0.1:8000"

service = Server(
    backend_server=f"{backend_address}",
    custom_templates={"Stat": StatTemplate},
)
```

### 启动服务

<div class="termy">

```console
$ pinfer sum_mnist:service --frontend-script=sum_mnist_frontend.py

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

并打开浏览器你会看到：

![INPUT](/assets/images/examples/custom-input-json.jpg)

### 调用后端并显示结果

添加以下高亮显示的代码以将请求发送到后端并显示结果。

```python title="frontend.py" linenums="1" hl_lines="23-32"
import json

import streamlit as st

from pinferencia.frontend.app import Server
from pinferencia.frontend.templates.base import BaseTemplate


class StatTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Numbers</span> '
        '<span style="color:slategray;">Statistics</span>'
    )

    def render(self):
        super().render()
        json_template = "[]"
        col1, col2 = st.columns(2)
        col2.write("Request Preview")
        raw_text = col1.text_area("Raw Data", value=json_template, height=150)
        col2.json(raw_text)

        pred_btn = st.button("Run") # (1)
        if pred_btn:
            with st.spinner("Wait for result"): # (2)
                prediction = self.predict(json.loads(raw_text)) # (3)
            st.write("Statistics")

            result_col1, result_col2, result_col3 = st.columns(3) # (4)
            result_col1.metric(label="Max", value=prediction.get("max"))
            result_col2.metric(label="Min", value=prediction.get("min"))
            result_col3.metric(label="Mean", value=prediction.get("mean"))


backend_address = "http://127.0.0.1:8000"

service = Server(
    backend_server=f"{backend_address}",
    custom_templates={"Stat": StatTemplate},
)

```

1. 提供一个按钮来触发预测。
2. 发送请求时显示一个等待效果。
3. 将数据发送到后端。
4. 将结果分为三列展示。

### 再次启动服务，您将看到：

![INPUT](/assets/images/examples/custom-template.jpg)
