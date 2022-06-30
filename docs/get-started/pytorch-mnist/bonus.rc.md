# 特殊任务

如果你还有时间，让我们尝试一些有趣的事情。

## MNIST 图像求和

让我们创建一个“sum_mnist.py”。 它接受一组图像，预测它们的数字并对它们求和。

在这里，我们首先创建一个自定义前端模板，接受两个 MNIST 图像并将它们发送回我们的后端进行预测。

### 自定义前端

!!! info "如何自定义模板？"
    您可以在 [自定义模板](../../../how-to-guides/custom-templates/) 找到更多信息。

#### 自定义模板

首先，我们需要一个新模板：


```python title="sum_mnist_frontend.py" linenums="1"
import base64

import streamlit as st
from PIL import Image

from pinferencia.frontend.templates.base import BaseTemplate
from pinferencia.frontend.templates.utils import display_text_prediction


class SumMnistTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Sum</span> '
        '<span style="color:slategray;">MNIST</span> '
    )

    def render(self):
        super().render()

        col1, col2 = st.columns(2) # (1)
        with col1.form("First Image", clear_on_submit=True):
            first_number = col1.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"], key="1"
            )

        with col2.form("Second Image", clear_on_submit=True):
            second_number = col2.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"], key="2"
            )

        st.markdown("##### Sum of the two digit:")
        images = []
        if first_number is not None: # (2)
            image1 = Image.open(first_number)
            col1.image(image1, use_column_width=True)
            images.append(base64.b64encode(first_number.getvalue()).decode())

        if second_number is not None: # (3)
            image1 = Image.open(second_number)
            col2.image(image1, use_column_width=True)
            images.append(base64.b64encode(second_number.getvalue()).decode())

        if first_number and second_number: # (4)
            with st.spinner("Waiting for result"):
                prediction = self.predict(images)
                display_text_prediction(prediction, component=st)
```

1. 这里我们将内容面板分成两列，每列接受一个 MNIST 图像。
2. 图像上传后，将其附加到图像数组中以供以后预测。
3. 图像上传后，将其附加到图像数组中以供以后预测。
4. 如果两张图片都上传了，发送到后端进行预测。

#### 自定义前端

在自定义模板文件的基础上，我们添加了一些额外的代码来自定义前端服务。

```python title="sum_mnist_frontend.py" linenums="1" hl_lines="6 49-54"
import base64

import streamlit as st
from PIL import Image

from pinferencia.frontend.app import Server
from pinferencia.frontend.templates.base import BaseTemplate
from pinferencia.frontend.templates.utils import display_text_prediction


class SumMnistTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Sum</span> '
        '<span style="color:slategray;">MNIST</span> '
    )

    def render(self):
        super().render()

        col1, col2 = st.columns(2)
        with col1.form("First Image", clear_on_submit=True):
            first_number = col1.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"], key="1"
            )

        with col2.form("Second Image", clear_on_submit=True):
            second_number = col2.file_uploader(
                "Choose an image...", type=["jpg", "png", "jpeg"], key="2"
            )

        st.markdown("##### Sum of the two digits:")
        images = []
        if first_number is not None:
            image1 = Image.open(first_number)
            col1.image(image1, use_column_width=True)
            images.append(base64.b64encode(first_number.getvalue()).decode())

        if second_number is not None:
            image1 = Image.open(second_number)
            col2.image(image1, use_column_width=True)
            images.append(base64.b64encode(second_number.getvalue()).decode())

        if first_number and second_number:
            with st.spinner("Waiting for result"):
                prediction = self.predict(images)
                display_text_prediction(prediction, component=st)


backend_address = "http://127.0.0.1:8000"

service = Server(
    backend_server=f"{backend_address}",
    custom_templates={"Sum Mnist": SumMnistTemplate},
)

```

### 后端

在我们自定义前端之后，我们可以在模型注册时直接使用我们自定义的模板。

```python title="sum_mnist.py" linenums="1" hl_lines="31-36 45"
import base64
import pathlib
from io import BytesIO

import torch
from PIL import Image
from pinferencia import Server
from pinferencia.handlers import BaseHandler
from torchvision import transforms

from main import Net


class MNISTHandler(BaseHandler):
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]
    )
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    def load_model(self):
        model = Net().to(self.device)
        model.load_state_dict(torch.load(self.model_path))
        model.eval()
        return model

    def predict(self, data: list) -> int:
        tensors = [] # (1)
        for img in data:
            image = Image.open(BytesIO(base64.b64decode(img)))
            tensors.append(self.transform(image))
        input_data = torch.stack(tensors).to(self.device)
        return sum(self.model(input_data).argmax(1).tolist())


service = Server(model_dir=pathlib.Path(__file__).parent.resolve())
service.register(
    model_name="mnist",
    model="mnist_cnn.pt",
    handler=MNISTHandler,
    load_now=True,
    metadata={"task": "Sum Mnist"}, # (2)
)

```

1. 这里我们对每张图像进行预处理，预测其数字并进行求和。
2. 将我们的新模板“Sum Mnist”注册为默认模板。

## 启动服务

<div class="termy">

```console
$ pinfer sum_mnist:service --frontend-script=sum_mnist_frontend.py

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

## 测试服务

![UI](/assets/images/examples/sum-mnist-ui.jpg)

玩得开心**Pinferencia**！
