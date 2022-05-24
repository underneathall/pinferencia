## 对于mac用户

如果你像我一样在 M1 Mac 上工作，你需要安装 `cmake` 和 `rust`

```bash
brew install cmake
```

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## 安装依赖

您可以使用 pip 安装依赖项。

```bash
pip install tqdm boto3 requests regex sentencepiece sacremoses transformers
```

或者您可以改用 docker 映像：

```bash
docker run -it -p 8000:8000 -v $(pwd):/opt/workspace huggingface/transformers-pytorch-cpu:4.18.0 bash
```
