import base64
import random
from io import BytesIO

from PIL import Image
from torchvision import datasets

dataset = datasets.MNIST(
    "./data",
    train=True,
    download=True,
    transform=None,
)
index = random.randint(0, len(dataset.data))
img = dataset.data[index]
img = Image.fromarray(img.numpy(), mode="L")

buffered = BytesIO()
img.save(buffered, format="JPEG")
base64_img_str = base64.b64encode(buffered.getvalue()).decode()
print("Base64 String:", base64_img_str)
print("target:", dataset.targets[index].tolist())
