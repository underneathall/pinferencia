<h1 align="center">
    Pinferencia
</h1>

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
</p>   
<p align="center">
    <em>Simple, but Powerful.</em>
</p>

---

<p align="center">
<a href="https://pinferencia.underneathall.app" target="_blank">
    English Doc
</a> | 
<a href="https://pinferencia.underneathall.app/zh" target="_blank">
    中文文档
</a> | 
<a href="https://pinferencia.underneathall.app/rc" target="_blank">
    不得不看版本-文档
</a>
</p>

---

**Pinferencia** tries to be the simplest AI model inference server ever!

Serving a model with REST API has never been so easy.

If you want to

- find a simple but robust way to serve your model
- write minimal codes while maintain controls over you service
- avoid any heavy-weight solutions
- easily to integrate with your CICD
- make your model and service portable and runnable across machines

You're at the right place.

## Features

**Pinferencia** features include:

- **Fast to code, fast to go alive**. Minimal codes needed, minimal transformation needed.
- **100% Test Coverage**: Both statement and branch coverages.
- **Easy to use, easy to understand**.
- **Automatic API documentation page**. All API explained in details with online try-out feature.
- **Serve any model**, even a single function can be served.

## Install

```bash
pip install "pinferencia[uvicorn]"
```

## Quick Start

**Serve Any Model**

```python title="app.py"
from pinferencia import Server


class MyModel:
    def predict(self, data):
        return sum(data)

model = MyModel()

service = Server()
service.register(
    model_name="mymodel",
    model=model,
    entrypoint="predict",
)
```
Just run:
```
uvicorn app:service --reload
```

Hooray, your service is alive. Go to http://127.0.0.1/ and have fun.

**Any Deep Learning Models?** Just as easy. Simple train or load your model, and register it with the service. Go alive immediately.

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
service.register(
    model_name="mymodel",
    model=model,
)
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
service.register(
    model_name="mymodel",
    model=model,
    entrypoint="predict",
)
```

Any model of any framework will just work the same way. Now run `uvicorn app:service --reload` and enjoy!


## Contributing

If you'd like to contribute, details are [here](./CONTRIBUTING.md)