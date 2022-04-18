# 欢迎使用Pinferencia

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/underneathall/pinferencia.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/underneathall/pinferencia/context:python)
[![codecov](https://codecov.io/gh/underneathall/pinferencia/branch/main/graph/badge.svg?token=M7J77E4IWC)](https://codecov.io/gh/underneathall/pinferencia)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/pinferencia.svg)](https://badge.fury.io/py/pinferencia)

## Pinferencia?

没听说过`Pinferencia`，这不是你的错。主要我的宣传经费，实在是不够多。

你是不是训练了一堆模型，然而别人谁用都不行。不是环境搞不定，就是bug命太硬。

你想:

> 要是我能有个API，谁能不陷入我的爱。不用安装不用等待，发个请求结果自己到来。

> 可是世上API千百万，却没有哪个我能玩得转。用来用去，看来还是我心太软，有些产品真的不能惯。

> 我多想这个世界变得简单，我的模型1分钟就能上线。然而现实这么残酷，一天两天过去，我的眼泪哗哗止不住。

> 到底谁能给予我这个恩赐啊，看来只有Pinferencia。

!!! tip "还嫌不够?"
    更多欢乐，请前往[正襟危坐版文档](/rc)

![Pinferencia](/asserts/images/examples/huggingface-vision.png)

<div class="termy">

```console
$ pip install "pinferencia[uvicorn]"
---> 100%
```

</div>

## Try it now!

### Create the App

=== "Scikit-Learn"

    ```python title="app.py"
    import joblib
    import uvicorn

    from pinferencia import Server


    # train your model
    model = "..."

    # or load your model
    model = joblib.load("/path/to/model.joblib") # (1)

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
        entrypoint="predict", # (2)
    )
    ```

    1. For more details, please visit https://scikit-learn.org/stable/modules/model_persistence.html

    2. `entrypoint` is the function name of the `model` to perform predictions.

        Here the data will be sent to the `predict` function: `model.predict(data)`.

=== "PyTorch"

    ```python title="app.py"
    import torch
    import uvicorn

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

    1. For more details, please visit https://pytorch.org/tutorials/beginner/saving_loading_models.html

=== "Tensorflow"

    ```python title="app.py"
    import tensorflow as tf
    import uvicorn

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

    1. For more details, please visit https://www.tensorflow.org/tutorials/keras/save_and_load

=== "HuggingFace Transformer"

    ```python title="app.py" linenums="1"
    from transformers import pipeline

    from pinferencia import Server

    vision_classifier = pipeline(task="image-classification")


    def predict(data):
        return vision_classifier(images=data)


    service = Server()
    service.register(model_name="vision", model=predict)

    ```

=== "Any Model"

    ```python title="app.py"
    import uvicorn

    from pinferencia import Server


    # train your models
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

=== "Any Function"

    ```python title="app.py"
    import uvicorn

    from pinferencia import Server

    # train your models
    def model(data):
        return sum(data)

    service = Server()
    service.register(
        model_name="mymodel",
        model=model,
    )
    ```

### Run!

<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>
