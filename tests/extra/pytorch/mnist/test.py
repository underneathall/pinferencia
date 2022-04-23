import random

import torch
from torchvision import datasets, transforms

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
)

dataset = datasets.MNIST(
    "../data",
    train=True,
    download=True,
    transform=transform,
)
index = random.randint(0, len(dataset.data))
img = dataset.data[index]
target = dataset.targets[index]
tensor = torch.Tensor([img.numpy()])


def test_entire_model():
    model = torch.load("entire_model.pt")
    model.eval()
    with torch.no_grad():
        data = torch.stack([tensor]).to("cpu")
        print("Prediction:", model(data).argmax(1).tolist()[0])
        print("Target:", target.numpy())


def test_torch_script():
    model = torch.jit.load("model_scripted.pt")
    model.eval()
    with torch.no_grad():
        data = torch.stack([tensor]).to("cpu")
        print("Prediction:", model(data).argmax(1).tolist()[0])
        print("Target:", target.numpy())


def test_state_dict():
    from main import Net

    device = "cpu"
    model = Net().to(device)
    state_dict = torch.load("state_dict.pt")
    model.load_state_dict(state_dict)
    model.eval()
    with torch.no_grad():
        data = torch.stack([tensor]).to("cpu")
        print("Prediction:", model(data).argmax(1).tolist()[0])
        print("Target:", target.numpy())


if __name__ == "__main__":
    print("=" * 10)
    print("Test Entire Model")
    test_entire_model()
    print("=" * 10)
    print("Test Torch Script")
    test_torch_script()
    print("=" * 10)
    print("Test State Dict")
    test_state_dict()
