import base64
from io import BytesIO

import torch
from main import Net
from PIL import Image
from torchvision import transforms

from pinferencia import Server

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ]
)


model = Net().to(device)
model.load_state_dict(torch.load("mnist_cnn.pt"))
model.eval()


def preprocessing(img_str):
    image = Image.open(BytesIO(base64.b64decode(img_str)))
    tensor = transform(image)
    return torch.stack([tensor]).to(device)


def predict(data):
    return model(preprocessing(data)).argmax(1).tolist()[0]


service = Server()
service.register(model_name="mnist", model=predict)
