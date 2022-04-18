# GPT2 - 文本生成转换器：如何使用和启动服务

什么是文本生成？输入一些文本，模型将预测后续文本会是什么。

听起来不错。不过不亲自尝试模型怎么可能有趣？

## 如何使用

模型将自动下载

```python
from transformers import pipeline, set_seed

generator = pipeline("text-generation", model="gpt2")
set_seed(42)


def predict(text):
    return generator(text, max_length=50, num_return_sequences=3)
```

**就是这样！**

让我们尝试一下：
```python
predict("You look amazing today,")
```

结果：

```
[{'generated_text': 'You look amazing today, guys. If you\'re still in school and you still have a job where you work in the field… you\'re going to look ridiculous by now, you\'re going to look really ridiculous."\n\nHe turned to his friends'},
 {'generated_text': 'You look amazing today, aren\'t you?"\n\nHe turned and looked at me. He had an expression that was full of worry as he looked at me. Even before he told me I\'d have sex, he gave up after I told him'},
 {'generated_text': 'You look amazing today, and look amazing in the sunset."\n\nGarry, then 33, won the London Marathon at age 15, and the World Triathlon in 2007, the two youngest Olympians to ride 100-meters. He also'}]
```

让我们看看第一个结果。
> You look amazing today, guys. If you're still in school and you still have a job where you work in the field… you're going to look ridiculous by now, you're going to look really ridiculous." 
> He turned to his friends

🤣 这就是我们要找的东西！如果再次运行预测，每次都会给出不同的结果。

## 如何部署

### 安装`Pinferencia`

<div class="termy">

```console
$ pip install "pinferencia[uvicorn]"
---> 100%
```

</div>

### 创建服务

```python title="app.py" linenums="1" hl_lines="3 13-14"
from transformers import pipeline, set_seed

from pinferencia import Server

generator = pipeline("text-generation", model="gpt2")
set_seed(42)


def predict(text):
    return generator(text, max_length=50, num_return_sequences=3)


service = Server()
service.register(model_name="gpt2", model=predict)

```

### 启动服务器

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
        'http://127.0.0.1:8000/v1/models/gpt2/predict' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
            "id": "string",
            "parameters": {},
            "data": "You look amazing today,"
        }'
    ```

    结果:
    
    ```json
    {
        "id": "string",
        "model_name": "gpt2",
        "data": [
            {
                "generated_text": "You look amazing today, I was in front of my friends. I wanted everyone to see me. But that's all. No one really cares about me in the eyes of the whole world unless I love them.\"\n\nIn a second Facebook post"
            },
            {
                "generated_text": "You look amazing today, and I know I am going to get the job done! So thank you all for all those donations, money, help, and hugs. I hope to see you again soon."
            },
            {
                "generated_text": "You look amazing today, but I will have to wait until early June for what will go down as the first NBA championship (a thing I had been expecting). If it's not the biggest, it is also not great. Now let's look at"
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
            "data": "You look amazing today,"
        },
    )
    print("Prediction:", response.json()["data"])
    ```

    运行`python test.py`并打印结果：

    ```
    Prediction: [
        {
            "generated_text": "You look amazing today, I was in front of my friends. I wanted everyone to see me. But that's all. No one really cares about me in the eyes of the whole world unless I love them.\"\n\nIn a second Facebook post"
        },
        {
            "generated_text": "You look amazing today, and I know I am going to get the job done! So thank you all for all those donations, money, help, and hugs. I hope to see you again soon."
        },
        {
            "generated_text": "You look amazing today, but I will have to wait until early June for what will go down as the first NBA championship (a thing I had been expecting). If it's not the biggest, it is also not great. Now let's look at"
        }
    ]
    ```

---

更酷的是，访问 http://127.0.0.1:8000，您将拥有一个交互式UI。

您可以在那里发送预测请求！
