import os
import pathlib
import random
import sys

import torch
from torchvision import datasets, transforms

sys.path.insert(0, os.getcwd())

from pinferencia.handlers import TorchEntireModelHandler  # noqa
from pinferencia.handlers import TorchScriptHandler  # noqa

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
)
work_dir = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, work_dir)
dataset = datasets.MNIST(
    f"{work_dir}/data",
    train=True,
    download=True,
    transform=transform,
)
index = random.randint(0, len(dataset.data))
img = dataset.data[index]
target = dataset.targets[index]
tensor = torch.Tensor([img.numpy()])
data = torch.stack([tensor]).to("cpu")


def test_entire_model():
    # define model path
    model_path = f"{work_dir}/entire_model.pt"

    # load using torch
    model = torch.load(model_path)
    model.eval()
    with torch.no_grad():
        print("Prediction:", model(data).argmax(1).tolist()[0])

    # load using handler
    handler = TorchEntireModelHandler(model_path=model_path)
    model = handler.load_model()

    # predict using handler
    handler.predict(data)
    print("Handler Prediction:", model(data).argmax(1).tolist()[0])


def test_torch_script():
    # define model path
    model_path = f"{work_dir}/model_scripted.pt"
    model = torch.jit.load(model_path)
    model.eval()
    with torch.no_grad():
        print("Prediction:", model(data).argmax(1).tolist()[0])

    # load using handler
    handler = TorchScriptHandler(model_path=model_path)
    model = handler.load_model()

    # predict using handler
    handler.predict(data)
    print("Handler Prediction:", model(data).argmax(1).tolist()[0])


def test_state_dict():
    from main import Net

    device = "cpu"
    model = Net().to(device)
    state_dict = torch.load(f"{work_dir}/state_dict.pt")
    model.load_state_dict(state_dict)
    model.eval()
    with torch.no_grad():
        print("Prediction:", model(data).argmax(1).tolist()[0])


if __name__ == "__main__":
    print("=" * 10)
    print("Target:", target.numpy())
    print("=" * 10)
    print("Test Entire Model")
    test_entire_model()
    print("=" * 10)
    print("Test Torch Script")
    test_torch_script()
    print("=" * 10)
    print("Test State Dict")
    test_state_dict()
