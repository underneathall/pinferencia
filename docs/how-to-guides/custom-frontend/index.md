# Custom Frontend Information

**Pinferencia** frontend supports customization on:

- title of the web page
- using model `display_name` as title on the template
- short description
- and detail description

## First Let's Create a Simple Model Service

```python title="app.py" linenums="1"
from typing import List

from pinferencia import Server


def stat(data: List[float]) -> float:
    return sum(data)


service = Server()
service.register(
    model_name="stat",
    model=stat,
    metadata={"display_name": "Awesome Model"}, # (1)
)

```

1. This will change the default templage title displayed on the right content area.

Now start the service:

<div class="termy">

```console
$ pinfer app:service

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

you will get:

![display name](/assets/images/examples/custom-frontend-display-name.jpg)

## Custom the Frontend

```python title="app.py" linenums="1"
from pinferencia.frontend.app import Server

detail_description = """
# My Awesome Model

This is the service of my awesome model.

It is **fast**, **simple**, and **beautiful**.

Visit [My Awesome Model Home](/abc) to learn more about it.
"""

service = Server(
    title="My Awesome Model", # (1)
    short_description="This is the short description", # (2)
    detail_description=detail_description, # (3)
    backend_server="http://127.0.0.1:8000",
)

```

1. This will change the title displayed on the top of the left side panel.
2. This will change the description below the title of the left side panel.
3. This will change the about information of the page.

Now start the service:

<div class="termy">

```console
$ pinfer app:service --frontend-script=frontend.py

Pinferencia: Frontend component streamlit is starting...
Pinferencia: Backend component uvicorn is starting...
```

</div>

you will get:

![display name](/assets/images/examples/custom-frontend.jpg)
