# 如何定义服务的请求和响应schema？

假设你有一个计算数据总和的服务。

它接受的请求内容是：
```json
[1, 2, 3]
```

返回的响应内容:

```json
6
```

您如何让用户知道您的请求和响应正文是什么样的？

如果您想自动验证或者解析请求和响应正文该怎么办？

本文，我们将介绍如何在 Pinferencia 中定义服务的请求和响应schema。

## Python 3 Type Hint

你听说过 python 中的“类型提示”吗？ 如果没有，您最好现在在 [Python Typing](https://docs.python.org/3/library/typing.html) 上查看。

从 Python 3.5 开始，Python 开始在函数定义中支持类型提示。 您可以声明参数的类型并返回。

**Pinferencia** 使用函数的类型提示来定义请求和响应的架构。 所以，你不需要学习另一种格式，你可以继续使用 python。

!!! warning "并非所有类型提示都受支持!"
     并非所有 python 中的类型提示都可以用来定义schema。 类型提示需要能够在 json schema中正确表示。

## Dummy 服务

让我们创建一个 Dummy 服务来向您展示一切是如何工作的。

```python title="dummy.py"
from pinferencia import Server

service = Server()


def dummy(data: list) -> str:
    return data


service.register(model_name="dummy", model=dummy)
```

启动服务，并访问后端文档页面，您将找到请求和响应的示例：

=== "请求示例"

    ```json
    {
        "id": "string",
        "parameters": {},
        "data": [
            "string"
        ]
    }
    ```

=== "响应示例"

    ```json
    {
        "id": "string",
        "model_name": "string",
        "model_version": "string",
        "parameters": {},
        "data": "string"
    }
    ```

这里函数参数的类型提示`list`将用于定义请求正文中的`data`字段。 函数返回的类型提示 `str` 将用于定义响应正文中的 `data` 字段。

## 求和服务

现在让我们回到本文开头提到的服务，一个求和服务：

=== "请求示例"

    ```json
    [1, 2, 3]
    ```

=== "响应示例"

    ```json
    6
    ```

让我们重写一下 Dummy 服务。

=== "Python 3.6及以上"

    ```python title="dummy.py"
    from typing import List

    from pinferencia import Server

    service = Server()


    def dummy(data: List[int]) -> int:
        return data


    service.register(model_name="dummy", model=dummy)
    ```

=== "Python 3.9及以上"

    ```python title="dummy.py"
    from pinferencia import Server

    service = Server()


    def dummy(data: list[int]) -> int:
        return sum(data)


    service.register(model_name="dummy", model=dummy)
    ```

现在访问后端文档页面，示例将是：

=== "请求示例"

    ```json
    {
        "id": "string",
        "parameters": {},
        "data": [
            0
        ]
    }
    ```

=== "响应示例"

    ```json
    {
        "id": "string",
        "model_name": "string",
        "model_version": "string",
        "parameters": {},
        "data": 0
    }
    ```

除了显示 schema 之外，**Pinferencia** 还验证并尝试将数据解析为所需的类型。 让我们在后端文档页面上试用 API。

=== "正常数据"

    === "请求"

        ```json
        {
            "id": "string",
            "parameters": {},
            "data": [
                1, 2, 3
            ]
        }
        ```

    === "响应"

        ```json
        {
            "id": "string",
            "model_name": "dummy",
            "model_version": "default",
            "data": 6
        }
        ```

=== "类型错误数据"

    让我们将请求中的数字之一更改为字符串类型。 该数字将根据 schema 自动转换为整数。

    === "请求"

        ```json
        {
            "id": "string",
            "parameters": {},
            "data": [
                "1", 2, 3
            ]
        }
        ```

    === "响应"

        ```json
        {
            "id": "string",
            "model_name": "dummy",
            "model_version": "default",
            "data": 6
        }
        ```

=== "错误数据"

    让我们发布一些无效的数据类型，您将收到一个 `422` 错误

    === "请求"

        ```json
        {
            "id": "string",
            "parameters": {},
            "data": 1
        }
        ```

    === "响应"

        ```json
        {
            "detail": [
                {
                "loc": [
                    "body",
                    "data"
                ],
                "msg": "value is not a valid list",
                "type": "type_error.list"
                }
            ]
        }
        ```

## 复杂的Schema

在 pydantic 的帮助下，可以在 Pinferencia 中定义复杂的schema。

让我们假设一个服务接收到个人信息：

```json title="请求"
[
    {
        "name": "Will",
        "age": 23,
        "gender": "male"
    },
    {
        "name": "Elise",
        "age": 19,
        "gender": "female"
    }
]
```

同时返回一个简单的欢迎问候。

```json title="响应"
"Hello, Will! Hello, Elise!"
```

让我们定义一下这个服务:

```python title="welcome.py"
from typing import List

from pydantic import BaseModel

from pinferencia import Server


class Person(BaseModel):
    name: str
    age: int
    gender: str


service = Server()


def welcome(persons: List[Person]) -> str:
    message = ""
    for person in persons:
        message += "Hello, " + person.name + "!"
    return message


service.register(model_name="welcome", model=welcome)
```

现在启动服务并访问后端文档页面，您会发现请求和响应示例如下：

=== "请求示例"

    ```json
    {
        "id": "string",
        "parameters": {},
        "data": [
            {
            "name": "string",
            "age": 0,
            "gender": "string"
            }
        ]
    }
    ```

=== "响应示例"

    ```json
    {
        "id": "string",
        "model_name": "string",
        "model_version": "string",
        "parameters": {},
        "data": "string"
    }
    ```

## 任务完成

您已经学习了如何使用 **Pinferencia** 定义请求和响应 Schema。 您现在可以尝试更多您感兴趣的 Schema。 玩得开心！
