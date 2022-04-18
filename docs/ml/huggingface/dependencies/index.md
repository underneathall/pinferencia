## For mac users

If you're working on a M1 Mac like me, you need install `cmake` and `rust`

```bash
brew install cmake
```

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Install dependencies

You can install dependencies using pip.

```bash
pip install tqdm boto3 requests regex sentencepiece sacremoses
```

or you can use a docker image instead:

```bash
docker run -it -p 8000:8000 -v $(pwd):/opt/workspace huggingface/transformers-pytorch-cpu:4.18.0 bash
```