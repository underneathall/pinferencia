# 上线 PyTorch MNIST 模型

在本教程中，我们将提供 PyTorch MNIST 模型。

它接收 Base64 编码的图像作为请求数据，并在响应中返回预测。

## 准备工作

访问 [PyTorch 示例 - MNIST](https://github.com/pytorch/examples/tree/main/mnist)，下载文件。

运行以下命令来安装和训练模型：

```bash
pip install -r requirements.txt
python main.py --save-model
```

训练完成后，您将拥有如下文件夹结构。创建了一个 `mnist_cnn.pt` 文件

```bash hl_lines="4"
.
├── README.md
├── main.py
├── mnist_cnn.pt
└── requirements.txt
```

## 部署方法

有两种方法可以部署模型。

- 直接注册一个函数。
- 仅使用附加处理程序 Handler 注册模型路径。

我们将在本教程中逐步介绍这两种方法。

## 直接注册一个函数

### 创建应用程序

让我们在同一个文件夹中创建一个文件 `func_app.py` 。

```python title="func_app.py" linenums="1"
import base64
from io import BytesIO

import torch
from main import Net # (1)
from PIL import Image
from torchvision import transforms

from pinferencia import Server, task

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ]
) # (2)


model = Net().to(device) # (3)
model.load_state_dict(torch.load("mnist_cnn.pt"))
model.eval()


def preprocessing(img_str):
    image = Image.open(BytesIO(base64.b64decode(img_str)))
    tensor = transform(image)
    return torch.stack([tensor]).to(device)


def predict(data):
    return model(preprocessing(data)).argmax(1).tolist()[0]


service = Server() # (4)
service.register(
    model_name="mnist",
    model=predict,
    metadata={"task": task.IMAGE_TO_TEXT},
)

```

1. 确保您可以导入网络模型。
2. 预处理转换代码。
3. 示例脚本只保存`state_dict`。这里我们需要初始化模型并加载`state_dict`。
4. 准备好，3、2、1。**GO！**

### 启动服务

=== "Only Backend"

    <div class="termy">

    ```console
    $ uvicorn func_app:service --reload
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
    $ pinfer func_app:service --reload

    Pinferencia: Frontend component streamlit is starting...
    Pinferencia: Backend component uvicorn is starting...
    ```

    </div>

### 测试服务

??? tip "测试数据那里来?"

    因为我们的输入是 base64 编码的 MNIST 图像，我们从哪里可以获得这些数据？

    您可以使用 PyTorch 的数据集。在同一文件夹中创建一个文件名为 `get-base64-img.oy` 。

    ```python title="get-base64-img.py"
    import base64
    import random
    from io import BytesIO

    from PIL import Image
    from torchvision import datasets

    dataset = datasets.MNIST( # (1)
        "./data",
        train=True,
        download=True,
        transform=None,
    )
    index = random.randint(0, len(dataset.data)) # (2)
    img = dataset.data[index]
    img = Image.fromarray(img.numpy(), mode="L")

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    base64_img_str = base64.b64encode(buffered.getvalue()).decode()
    print("Base64 String:", base64_img_str) # (3)
    print("target:", dataset.targets[index].tolist())

    ```

    1. 这是训练期间使用的 MNIST 数据集。
    2. 让我们使用随机图像。
    3. 字符串和目标被打印到标准输出。

    **运行脚本并复制字符串。**

    ```bash
    python get-base64-img.py
    ```

    输出:

    ```bash
    Base64 String: /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+uhfwXqy2Ph25VYnPiB3SzhUkPlXCfNkAAEsCCCeOeKx9RsLjStUu9Ou1C3NpM8Eqg5AdSVIz35FVqK9xl0HXhb/C20sdMubjTLMQXs11AhkRXmmDsCwzgAYPpz+XI/GrSLrTfiVqNzPapbw3xE8AWQNvUAKXOOmWVjg+teeUV2fgXxd4hsPE2hWEGuX8Vh9uhja3Fw3lbGcBhtzjGCad8XI7iL4p68twHDGcMm45+QqCuPbBFcVRRU97fXepXb3d9dT3VzJjfNPIXdsAAZY8nAAH4VBX/9k=
    target: 4
    ```

#### 前端界面

打开http://127.0.0.1:8501，会自动选择模板`Image to Text`。

使用下图：

![mnist 4](/assets/images/examples/mnist-4.png)

你会得到：

![UI](/assets/images/examples/mnist-ui.jpg)

#### 后端API

让我们创建一个文件`test.py`

```python title="test.py" linenums="1"
import requests

response = requests.post(
    url="http://localhost:8000/v1/models/mnist/predict",
    json={"data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+uhfwXqy2Ph25VYnPiB3SzhUkPlXCfNkAAEsCCCeOeKx9RsLjStUu9Ou1C3NpM8Eqg5AdSVIz35FVqK9xl0HXhb/C20sdMubjTLMQXs11AhkRXmmDsCwzgAYPpz+XI/GrSLrTfiVqNzPapbw3xE8AWQNvUAKXOOmWVjg+teeUV2fgXxd4hsPE2hWEGuX8Vh9uhja3Fw3lbGcBhtzjGCad8XI7iL4p68twHDGcMm45+QqCuPbBFcVRRU97fXepXb3d9dT3VzJjfNPIXdsAAZY8nAAH4VBX/9k="},
)
print("Prediction:", response.json()["data"])

```

**运行测试:**

<div class="termy">

```console
$ python test.py
Prediction: 4
```

</div>


您可以尝试使用更多图像来测试，甚至可以使用交互式 API 文档页面 http://127.0.0.1:8000


## 使用 Handler 注册模型路径

!!! tip "Handler"
    如果您更喜欢使用文件提供模型的经典方式，则使用“Handlers”是您的选择。

    处理程序的详细信息，请访问 [**Handlers**](/handlers)

### 创建应用程序

让我们在同一个文件夹中创建一个文件 func_app.py 。

下面的代码被重构为 MNISTHandler 。看起来更干净！

```python title="path_app.py" linenums="1"
import base64
import pathlib
from io import BytesIO

import torch
from main import Net
from PIL import Image
from torchvision import transforms

from pinferencia import Server, task
from pinferencia.handlers import BaseHandler


class MNISTHandler(BaseHandler):
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]
    )
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    def load_model(self): # (1)
        model = Net().to(self.device)
        model.load_state_dict(torch.load(self.model_path))
        model.eval()
        return model

    def predict(self, data): # (2)
        image = Image.open(BytesIO(base64.b64decode(data)))
        tensor = self.transform(image)
        input_data = torch.stack([tensor]).to(self.device)
        return self.model(input_data).argmax(1).tolist()[0]


service = Server(model_dir=pathlib.Path(__file__).parent.resolve()) # (3)
service.register(
    model_name="mnist",
    model="mnist_cnn.pt",
    handler=MNISTHandler,
    load_now=True, # (4)
    metadata={"task": task.IMAGE_TO_TEXT},
)

```

1. 我们将加载模型的代码移到`load_model`函数中。模型路径可以通过 `self.model_path` 访问。

2. 我们将预测代码移到`predict`函数中。该模型可以通过`self.model`访问。

3. `model_dir` 是 `Pinferencia` 查找模型文件的地方。将 model_dir 设置为包含 `mnist_cnn.pt` 和此脚本的文件夹。

4. `load_now` 确定模型是否会在注册期间立即加载。默认值为“真”。如果设置为 `False`，则需要调用 `load` API 加载模型才能进行预测。

### 启动服务

=== "Only Backend"

    <div class="termy">

    ```console
    $ uvicorn func_app:service --reload
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
    $ pinfer func_app:service --reload

    Pinferencia: Frontend component streamlit is starting...
    Pinferencia: Backend component uvicorn is starting...
    ```

    </div>

### 测试服务

**运行测试:**

<div class="termy">

```console
$ python test.py
Prediction: 4
```

</div>

不出意外，结果一样。


## 最后

使用 **Pinferencia**，您可以为任何模型提供服务。

您可以自己加载模型，就像您在进行离线预测时所做的那样。 **这部分代码你早就已经写好了。**

然后，只需使用 **Pinferencia** 注册模型，您的模型就会生效。

或者，您可以选择将代码重构为 **Handler Class**。旧的经典方式也适用于 **Pinferencia**。

这两个世界都适用于您的模型，**经典​​音乐** 和 **摇滚乐**。

是不是很棒！

---

现在您已经掌握了如何使用 **Pinferencia** 来：

- 注册任何模型、任何函数并把它们上线。
- 使用您的自定义处理程序为您的机器学习模型提供服务。
