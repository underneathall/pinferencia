# Bonus

If you still have time, let's try something fun.

## Extra: Sum Up the MNIST Images

Let's create a `sum_mnist.py`. It accepts an array of images, predicts their digits and sum up them.

Here, we first create a custom frontend template accepting two MNIST images and send them back to our backend for prediction.

### Custom Frontend

!!! info "How to Custom Template?"
    You can find more info at [Custom Templates](../../../how-to-guides/custom-templates/).

#### Custom Template

First, we need a new template:

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

1. Here we split the content panel into two columns, each accepts a single MNIST image.
2. Once the image is uploaded, append it to the image array for later prediction.
3. Once the image is uploaded, append it to the image array for later prediction.
4. If both images are uploaded, send them to backend to predict.

#### Custom Frontend

Based on the custom template file, we add some extra lines to define the custom frontend service.

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

### Backend

After we customize the frontend, we can directly use our custom template during model registration.

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

1. Here we pre-process each image, predict its digit and sum up.
2. Register our new template `Sum Mnist` as the default template.

## Start the Service

<div class="termy">

```console
$ pinfer sum_mnist:service --frontend-script=sum_mnist_frontend.py

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

## Test the Service

![UI](/assets/images/examples/sum-mnist-ui.jpg)

Have fun with **Pinferencia**!
