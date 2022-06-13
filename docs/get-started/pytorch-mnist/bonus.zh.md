# 特殊任务

如果你还有时间，让我们尝试一些有趣的事情。

## 额外： MNIST 图像的加法

让我们创建一个“sum_mnist.py”。它接受一组图像，预测它们的数字并把它们加起来。

```python title="sum_mnist.py" linenums="1" hl_lines="31-36"
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

    def load_model(self):
        model = Net().to(self.device)
        model.load_state_dict(torch.load(self.model_path))
        model.eval()
        return model

    def predict(self, data):
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
    metadata={"task": task.IMAGE_TO_TEXT},
)

```

1. 这里我们对每张图像进行预处理，预测其位数并进行总结。

希望你在 **Pinferencia** 世界玩得开心！
