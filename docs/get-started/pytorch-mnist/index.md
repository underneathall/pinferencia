# Serve PyTorch MNIST Model

In this tutorial, we will serve a PyTorch MNIST model.

It receives a Base64 encoded image as request data, and return the prediction in the response.

## Prerequisite

Visit [PyTorch Examples - MNIST](https://github.com/pytorch/examples/tree/main/mnist), download the files.

Run below commands to install and train the model:

```bash
pip install -r requirements.txt
python main.py --save-model
```

After the training is finished, you will have a folder structure as below. A `mnist_cnn.pt` file is created

```bash hl_lines="4"
.
├── README.md
├── main.py
├── mnist_cnn.pt
└── requirements.txt
```

## Deploy Methods

There are two methods you can deploy the model.

- Directly register a function.
- Only register a model path, with an additioanl handler.

We will cover both methods step by step in this tutorial.

## Directly Register a Function

### Create the App

Let's create a file `func_app.py` in the same folder.

```python title="func_app.py" linenums="1"
import base64
from io import BytesIO

import torch
from main import Net # (1)
from PIL import Image
from torchvision import transforms

from pinferencia import Server

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
service.register(model_name="mnist", model=predict)

```

1. Make suer you can import the Net Model.
2. Preprocessing transformation codes.
3. The example script only save the `state_dict`. Here we need to initialize the model and load the `state_dict`.
4. Get ready, 3, 2, 1. **GO!**

### Start the Service

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

### Test the Service

??? tip "Test Data?"
    Because our input is a base64 encoded MNIST image, where can we get these data?

    You can make use of PyTorch's datasets. Create a file with in the same folder named `get-base64-img`.

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

    1. This is the MNIST dataset used during training.
    2. Let's use a random image.
    3. The string and the target are printed to stdout.

    **Run the script and copy the string.**

    ```bash
    python get-base64-img.py
    ```

    Output:

    ```bash
    Base64 String: /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+uhfwXqy2Ph25VYnPiB3SzhUkPlXCfNkAAEsCCCeOeKx9RsLjStUu9Ou1C3NpM8Eqg5AdSVIz35FVqK9xl0HXhb/C20sdMubjTLMQXs11AhkRXmmDsCwzgAYPpz+XI/GrSLrTfiVqNzPapbw3xE8AWQNvUAKXOOmWVjg+teeUV2fgXxd4hsPE2hWEGuX8Vh9uhja3Fw3lbGcBhtzjGCad8XI7iL4p68twHDGcMm45+QqCuPbBFcVRRU97fXepXb3d9dT3VzJjfNPIXdsAAZY8nAAH4VBX/9k=
    target: 4
    ```

Let's create a file `test.py`

```python title="test.py" linenums="1"
import requests

response = requests.post(
    url="http://localhost:8000/v1/models/mnist/predict",
    json={"data": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+uhfwXqy2Ph25VYnPiB3SzhUkPlXCfNkAAEsCCCeOeKx9RsLjStUu9Ou1C3NpM8Eqg5AdSVIz35FVqK9xl0HXhb/C20sdMubjTLMQXs11AhkRXmmDsCwzgAYPpz+XI/GrSLrTfiVqNzPapbw3xE8AWQNvUAKXOOmWVjg+teeUV2fgXxd4hsPE2hWEGuX8Vh9uhja3Fw3lbGcBhtzjGCad8XI7iL4p68twHDGcMm45+QqCuPbBFcVRRU97fXepXb3d9dT3VzJjfNPIXdsAAZY8nAAH4VBX/9k="},
)
print("Prediction:", response.json()["data"])

```

**Run the test:**

<div class="termy">

```console
$ python test.py
Prediction: 4
```

</div>

You can try out the API with more images, or even using the interactive API documentation page http://127.0.0.1


## Register a Model Path, with a Handler

!!! tip "Handler"
    If you prefer the old classical way of serving a model with a file, using a `handler` is your choice.

    For details of handlers, please visit [**Handlers**](/src/handlers)

### Create the App

Let's create a file `func_app.py` in the same folder.

The codes below are refactored into a handle class. It looks cleaner!

```python title="path_app.py" linenums="1"
import base64
import pathlib
from io import BytesIO

import torch
from main import Net
from PIL import Image
from torchvision import transforms

from pinferencia import Server
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
)

```

1. We move the codes of loading the model into the `load_model` function. The model path can be accessed by `self.model_path`.

2. We move the codes of predicting into the `predict` function. The model can be accessed by `self.model`.

3. `model_dir` is where `Pinference` will look for your model files. Set the model_dir to the folder having the `mnist_cnn.pt` and this script.

4. `load_now` determine if the model will be get loaded immediately during registration. The default is `True`. If set to `False`, you need to call the `load` API to load the model before prediction.

### Start the Service

<div class="termy">

```console
$ uvicorn path_app:service --reload
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using statreload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

### Test the Service

**Run the test:**

<div class="termy">

```console
$ python test.py
Prediction: 4
```

</div>

No suprise, the same result.


## In the End

Using **Pinferencia**, you can serve any model.

You can load the models by yourself, just what you have done to do a offline prediction. **The codes are already there.**

Then, just register the model using **Pinferencia**, and your model is alive.

Alternatively, you can choose to refactor your codes into a **Handler Class**. The old classic way also works with **Pinferencia**.

Both worlds work for your model, **classic music** and **rock'n'roll**.

Isn't it great!

Now you have mastered how to use **Pinference** to:

- Register any model, any function and serve them.
- Use your custom handler to serve your machine learning model.

If you still have time, let's try something fun in the next tutorial.