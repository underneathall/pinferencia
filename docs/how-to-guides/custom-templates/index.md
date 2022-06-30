# Custom Templates

Although there are built-in templates, it will never be enough to cover all the scenanrios.

**Pinferencia** supports custom templates. It's easy to customize a template and use it in your service.

First let's try to create a simple template:

1. Input a list of numbers.
2. Display the mean, max and min of the numbers.

## Model

The model is simple, and the service can be defined as:

```python title="app.py" linenums="1"
from typing import List

from pinferencia import Server


def stat(data: List[float]) -> dict:
    return {
        "mean": sum(data) / len(data),
        "max": max(data),
        "min": min(data),
    }


service = Server()
service.register(model_name="stat", model=stat, metadata={"task": "Stat"})
```

## Template

**Pinferencia** provides a `BaseTemplate` to extend on to build a custom template.

### JSON Input Field

First, we create a JSON input field and display field in two columns.

```python title="frontend.py" linenums="1"
import streamlit as st

from pinferencia.frontend.app import Server
from pinferencia.frontend.templates.base import BaseTemplate


class StatTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Numbers</span> '
        '<span style="color:slategray;">Statistics</span>'
    )

    def render(self):
        super().render()
        json_template = "[]"
        col1, col2 = st.columns(2)
        col2.write("Request Preview")
        raw_text = col1.text_area("Raw Data", value=json_template, height=150)
        col2.json(raw_text)


backend_address = "http://127.0.0.1:8000"

service = Server(
    backend_server=f"{backend_address}",
    custom_templates={"Stat": StatTemplate},
)
```

### Start the Service

<div class="termy">

```console
$ pinfer sum_mnist:service --frontend-script=sum_mnist_frontend.py

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

And open the browser you will see:

![INPUT](/assets/images/examples/custom-input-json.jpg)

### Call Backend and Display Results

Add the below highlighted codes to send request to backend and display the result.

```python title="frontend.py" linenums="1" hl_lines="23-32"
import json

import streamlit as st

from pinferencia.frontend.app import Server
from pinferencia.frontend.templates.base import BaseTemplate


class StatTemplate(BaseTemplate):
    title = (
        '<span style="color:salmon;">Numbers</span> '
        '<span style="color:slategray;">Statistics</span>'
    )

    def render(self):
        super().render()
        json_template = "[]"
        col1, col2 = st.columns(2)
        col2.write("Request Preview")
        raw_text = col1.text_area("Raw Data", value=json_template, height=150)
        col2.json(raw_text)

        pred_btn = st.button("Run") # (1)
        if pred_btn:
            with st.spinner("Wait for result"): # (2)
                prediction = self.predict(json.loads(raw_text)) # (3)
            st.write("Statistics")

            result_col1, result_col2, result_col3 = st.columns(3) # (4)
            result_col1.metric(label="Max", value=prediction.get("max"))
            result_col2.metric(label="Min", value=prediction.get("min"))
            result_col3.metric(label="Mean", value=prediction.get("mean"))


backend_address = "http://127.0.0.1:8000"

service = Server(
    backend_server=f"{backend_address}",
    custom_templates={"Stat": StatTemplate},
)

```

1. Display a button to trigger prediction.
2. Display a spinner while sending the request.
3. Send the data to backend.
4. Display the results in 3 columns.

### Start the Service again, and You Will Get:

![INPUT](/assets/images/examples/custom-template.jpg)
