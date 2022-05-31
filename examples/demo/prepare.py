import nltk
import torch
from pytorch_pretrained_biggan import BigGAN
from transformers import pipeline

nltk.download("wordnet")
nltk.download("omw-1.4")

image_classification_save_path = "/tmp/google-vit"
tranlator_save_path = "/tmp/google-t5"

classifier = pipeline(model="google/vit-base-patch16-224")
translator = pipeline(model="t5-base", tokenizer="t5-base")

classifier.save_pretrained(image_classification_save_path)
translator.save_pretrained(tranlator_save_path)

BigGAN.from_pretrained("biggan-deep-256")

torch.hub.load(
    "AK391/animegan2-pytorch:main",
    "generator",
    pretrained=True,
    device="cpu",
    progress=False,
)
torch.hub.load(
    "AK391/animegan2-pytorch:main",
    "face2paint",
    size=512,
    device="cpu",
    side_by_side=False,
)
