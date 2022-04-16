Many of you must have heard of `Bert`, or `transformers`.
And you may also know huggingface.

In this tutorial, let's play with its pytorch transformer model and serve it through REST API

## How does the model work?

With an input of an incomplete sentence, the model will give its prediction:

=== "Input"

    ```
    Paris is the [MASK] of France.
    ```

=== "Output"

    ```
    Paris is the capital of France.
    ```

Cool~ Let's try it out now~

## Prerequisite

### For mac users

If you're working on a M1 Mac like me, you need install `cmake` and `rust`

```bash
brew install cmake
```

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Install dependencies

You can install dependencies using pip.

```bash
pip install tqdm boto3 requests regex sentencepiece sacremoses
```

or you can use a docker image instead:

```bash
docker run -it -p 8000:8000 -v $(pwd):/opt/workspace huggingface/transformers-pytorch-cpu:4.18.0 bash
```

## Load the model

This will load the tokenizer and the model. It may take sometime to download.

```python
import torch

# load tokenizer
tokenizer = torch.hub.load(
    "huggingface/pytorch-transformers",
    "tokenizer",
    "bert-base-cased",
)
# load masked model
masked_lm_model = torch.hub.load(
    "huggingface/pytorch-transformers",
    "modelForMaskedLM",
    "bert-base-cased",
)
```

## Define the predict function

The input text is: Paris is the [MASK] of France.
```python
input_text = "Paris is the [MASK] of France."
```

First we need to tokenize the 
```python
tokens = tokenizer(input_text)
```

Let's have a look at the masked index:
```python
mask_index = [
    i
    for i, token_id in enumerate(tokens["input_ids"])
    if token_id == tokenizer.mask_token_id
]
```

Prepare the tensor:
```python
segments_tensors = torch.tensor([tokens["token_type_ids"]])
tokens_tensor = torch.tensor([tokens["input_ids"]])
```

Predict:
```python
with torch.no_grad():
    predictions = masked_lm_model(
        tokens_tensor, token_type_ids=segments_tensors
    )
```

Now, let's have a look at the result:

```python
pred_tokens = torch.argmax(predictions[0][0], dim=1)

# replace the initail input text's mask with predicted text
for i in mask_index:
    tokens["input_ids"][i] = pred_tokens[i]
tokenizer.decode(tokens["input_ids"], skip_special_tokens=True)
```

Output:

```
'Paris is the capital of France.'
```

**Let's organize the codes in to a predict function**:


```python title="predict" linenums="1"
import torch

# load tokenizer
tokenizer = torch.hub.load(
    "huggingface/pytorch-transformers",
    "tokenizer",
    "bert-base-cased",
)
# load masked model
masked_lm_model = torch.hub.load(
    "huggingface/pytorch-transformers",
    "modelForMaskedLM",
    "bert-base-cased",
)
def predict(input_text):
    # tokenize the input text
    tokens = tokenizer(input_text)

    # get all the mask index
    mask_index = [
        i
        for i, token_id in enumerate(tokens["input_ids"])
        if token_id == tokenizer.mask_token_id
    ]

    # convert the input ids and type ids to tensor
    segments_tensors = torch.tensor([tokens["token_type_ids"]])
    tokens_tensor = torch.tensor([tokens["input_ids"]])

    # run predictions
    with torch.no_grad():
        predictions = masked_lm_model(
            tokens_tensor, token_type_ids=segments_tensors
        )

    # pick the most likely predictions

    pred_tokens = torch.argmax(predictions[0][0], dim=1)

    # replace the initail input text's mask with predicted text
    for i in mask_index:
        tokens["input_ids"][i] = pred_tokens[i]
    return tokenizer.decode(tokens["input_ids"], skip_special_tokens=True)
```

Predict:

=== "Codes"
    ```python
    predict("Paris is the [MASK] of France.")
    ```

=== "Output"

    ```
    'Paris is the capital of France.'
    ```

## Serve it through REST API

### Install Pinferencia

First, let's install [Pinferencia](https://github.com/underneathall/pinferencia).

```bash
pip install "pinferencia[uvicorn]"
```

### Create app.py

Let's save our predict function into a file `app.py` and add some lines to register it.

```python title="app.py" linenums="1" hl_lines="2 48-49"
import torch
from pinferencia import Server

# load tokenizer
tokenizer = torch.hub.load(
    "huggingface/pytorch-transformers",
    "tokenizer",
    "bert-base-cased",
)
# load masked model
masked_lm_model = torch.hub.load(
    "huggingface/pytorch-transformers",
    "modelForMaskedLM",
    "bert-base-cased",
)


def predict(input_text):
    # tokenize the input text
    tokens = tokenizer(input_text)

    # get all the mask index
    mask_index = [
        i
        for i, token_id in enumerate(tokens["input_ids"])
        if token_id == tokenizer.mask_token_id
    ]

    # convert the input ids and type ids to tensor
    segments_tensors = torch.tensor([tokens["token_type_ids"]])
    tokens_tensor = torch.tensor([tokens["input_ids"]])

    # run predictions
    with torch.no_grad():
        predictions = masked_lm_model(
            tokens_tensor, token_type_ids=segments_tensors
        )

    # pick the most likely predictions
    pred_tokens = torch.argmax(predictions[0][0], dim=1)

    # replace the initail input text's mask with predicted text
    for i in mask_index:
        tokens["input_ids"][i] = pred_tokens[i]
    return tokenizer.decode(tokens["input_ids"], skip_special_tokens=True)


service = Server()
service.register(model_name="transformer", model=predict)

```

Run the service, and wait for it to load the model and start the server:
<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Test the service

=== "curl"

    **Request**

    ```bash
    curl --location --request POST \
        'http://127.0.0.1:8000/v1/models/transformer/predict' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "data": "Paris is the [MASK] of France."
        }'
    ```

    **Response**

    ```
    {
        "model_name":"transformer",
        "data":"Paris is the capital of France."
    }
    ```

=== "Python Requests"

    **Create the `test.py`.**

    ```python title="test.py" linenums="1"
    import requests


    response = requests.post(
        url="http://localhost:8000/v1/models/transformer/predict",
        json={"data": "Paris is the [MASK] of France."},
    )
    print(response.json())

    ```
    **Run the script and check the result.**

    <div class="termy">

    ```console
    $ python test.py
    {'model_name': 'json', 'data': 'Paris is the capital of France.'}
    ```

    </div>
 
 
 
