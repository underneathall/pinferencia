你们中的许多人一定听说过“Bert”或“transformers”。
你可能还知道 **HuggingFace**。

在本教程中，让我们使用它的 pytorch 转换器模型并通过 REST API 为它提供服务

## 模型是如何工作的？

输入一个不完整的句子，模型将给出它的预测：

=== "Input"

    ```
    Paris is the [MASK] of France.
    ```

=== "Output"

    ```
    Paris is the capital of France.
    ```

酷~ 现在就来试试吧~

## 先决条件

### 对于mac用户

如果你像我一样在 M1 Mac 上工作，你需要安装 `cmake` 和 `rust`

```bash
brew install cmake
```

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 安装依赖

您可以使用 pip 安装依赖项。

```bash
pip install tqdm boto3 requests regex sentencepiece sacremoses
```

或者您可以改用 docker 镜像：

```bash
docker run -it -p 8000:8000 -v $(pwd):/opt/workspace huggingface/transformers-pytorch-cpu:4.18.0 bash
```

## 加载模型

这将加载标记器和模型。 下载可能需要一些时间。

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

## 定义预测函数

输入文本是: Paris is the [MASK] of France.
```python
input_text = "Paris is the [MASK] of France."
```

首先，我们需要进行tokenize
```python
tokens = tokenizer(input_text)
```

让我们看一下掩码的索引：
```python
mask_index = [
    i
    for i, token_id in enumerate(tokens["input_ids"])
    if token_id == tokenizer.mask_token_id
]
```

准备张量：
```python
segments_tensors = torch.tensor([tokens["token_type_ids"]])
tokens_tensor = torch.tensor([tokens["input_ids"]])
```

预测：
```python
with torch.no_grad():
    predictions = masked_lm_model(
        tokens_tensor, token_type_ids=segments_tensors
    )
```

现在，让我们看看结果：

```python
pred_tokens = torch.argmax(predictions[0][0], dim=1)

# replace the initail input text's mask with predicted text
for i in mask_index:
    tokens["input_ids"][i] = pred_tokens[i]
tokenizer.decode(tokens["input_ids"], skip_special_tokens=True)
```

输出:

```
'Paris is the capital of France.'
```

**让我们将代码组织到一个预测函数中**：


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

预测:

=== "Codes"
    ```python
    predict("Paris is the [MASK] of France.")
    ```

=== "Output"

    ```
    'Paris is the capital of France.'
    ```

## 通过 REST API 提供服务

### 安装 Pinferencia

首先，让我们安装 [Pinferencia](https://github.com/underneathall/pinferencia).

```bash
pip install "pinferencia[uvicorn]"
```

### 创建app.py

让我们将我们的预测函数保存到一个文件 `app.py` 中并添加一些代码来注册这个模型。

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

运行服务，等待它加载模型并启动服务器：
<div class="termy">

```console
$ uvicorn app:service --reload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### 测试服务

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
