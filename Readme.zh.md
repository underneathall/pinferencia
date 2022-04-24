![Pinferencia](/docs/asserts/images/logo_header.png)

<p align="center">
    <em>简单，但功能强大。</em>
</p>

<p align="center">
    <a href="https://lgtm.com/projects/g/underneathall/pinferencia/context:python">
        <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/underneathall/pinferencia.svg?logo=lgtm&logoWidth=18"/>
    </a>
    <a href="https://codecov.io/gh/underneathall/pinferencia">
        <img src="https://codecov.io/gh/underneathall/pinferencia/branch/main/graph/badge.svg?token=M7J77E4IWC"/>
    </a>
    <a href="https://opensource.org/licenses/Apache-2.0">
        <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/>
    </a>
    <a href="https://pypi.org/project/pinferencia/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/pinferencia?color=green">
    </a>
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pinferencia">
</p>

---

<p align="center">
<a href="https://pinferencia.underneathall.app/zh" target="_blank">
    中文文档
</a> |
<a href="https://pinferencia.underneathall.app" target="_blank">
    English Doc
</a> |
<a href="./Readme.md" target="_blank">
    English Readme
</a>
</p>

<p align="center">
     <em>急需帮助。 翻译，说唱歌词，统统都要。</em>
</p>

---

**Pinferencia** 致力成为最简单的机器学习推理服务器！

**只需要三行代码，模型即刻上线**。

使用 REST API 部署模型从未如此简单。

![Pinferencia](/docs/asserts/images/examples/huggingface-vision.png)

如果你想

- 找到一种**简单但强大**的方式来为您的模型提供服务
- 编写**最少**代码，同时保持对您服务的控制权
- **避免**任何**重量级**解决方案
- **兼容**与其他工具/平台

那你来对地方了。

## Pinferencia?

没听说过`Pinferencia`，这不是你的错。主要我的宣传经费，实在是不够多。

你是不是训练了一堆模型，然而别人谁用都不行。不是环境搞不定，就是bug命太硬。

你想:

> 要是我能有个API，谁能不陷入我的爱。不用安装不用等待，发个请求结果自己到来。

> 可是世上API千百万，却没有哪个我能玩得转。用来用去，看来还是我心太软，有些产品真的不能惯。

> 我多想这个世界变得简单，我的模型1分钟就能上线。然而现实这么残酷，一天两天过去，我的眼泪哗哗止不住。

> 到底谁能给予我这个恩赐啊，看来只有Pinferencia。

## 特征

**Pinferencia** 功能包括：

- **快速编码，快速上线**。 需要最少的代码，需要最少的转换。仅仅基于你已有的代码。
- **100% 测试覆盖率**：包括语句和分支覆盖率，绝对不开玩笑。 您是否知道任何模型服务工具经过如此严格的测试？
- **易于使用，易于理解**。
- **自动 API 文档页面**。 所有 API 都有在线调试功能且包括了详细的解释。
- **部署任何模型**，甚至可以部署单个函数。
- **支持 Kserve API**，兼容 Kubeflow、TF Serving、Triton 和 TorchServe。 切换到它们或从它们切换过来，几乎没有开销，而且 **Pinferencia** 用来调试模型和做demo要方便得多！

## 安装

```bash
pip install "pinferencia[uvicorn]"
```

## 快速开始

**部署任何模型**

```python title="app.py"
from pinferencia import Server


class MyModel:
    def predict(self, data):
        return sum(data)


model = MyModel()

service = Server()
service.register(model_name="mymodel", model=model, entrypoint="predict")
```

只需运行:

```
uvicorn app:service --reload
```

就这么简单，你的模型活起来了。 去 http://127.0.0.1:8000/ 看下吧，祝你玩得开心。

**其它深度学习模型？**同样简单。 只需要训练或加载您的模型，并将其注册到服务中，立刻就能上线。

**Hugging Face**

具体请看: [HuggingFace Pipeline - Vision](https://pinferencia.underneathall.app/ml/huggingface/pipeline/vision/)

```python title="app.py" linenums="1"
from transformers import pipeline

from pinferencia import Server

vision_classifier = pipeline(task="image-classification")


def predict(data):
    return vision_classifier(images=data)


service = Server()
service.register(model_name="vision", model=predict)

```

**Pytorch**

```python title="app.py"
import torch

from pinferencia import Server


# train your models
model = "..."

# or load your models (1)
# from state_dict
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH))

# entire model
model = torch.load(PATH)

# torchscript
model = torch.jit.load('model_scripted.pt')

model.eval()

service = Server()
service.register(model_name="mymodel", model=model)
```

**Tensorflow**

```python title="app.py"
import tensorflow as tf

from pinferencia import Server


# train your models
model = "..."

# or load your models (1)
# saved_model
model = tf.keras.models.load_model('saved_model/model')

# HDF5
model = tf.keras.models.load_model('model.h5')

# from weights
model = create_model()
model.load_weights('./checkpoints/my_checkpoint')
loss, acc = model.evaluate(test_images, test_labels, verbose=2)

service = Server()
service.register(model_name="mymodel", model=model, entrypoint="predict")
```

任何框架的任何模型都将以相同的方式工作。 现在运行 `uvicorn app:service --reload` 来感受魔法吧！


## 想要帮助我？

如果你想提供帮助，可以参考 [这里](./CONTRIBUTING.md)