import base64
from io import BytesIO

import torch
from PIL import Image
from pytorch_pretrained_biggan import (
    BigGAN,
    convert_to_images,
    one_hot_from_names,
    truncated_noise_sample,
)
from transformers import pipeline

from pinferencia import Server, task


def load_model():
    image_classification_save_path = "/tmp/google-vit"
    tranlator_save_path = "/tmp/google-t5"
    return (
        pipeline(task="image-classification", model=image_classification_save_path),
        pipeline(
            task="translation",
            model=tranlator_save_path,
            tokenizer=tranlator_save_path,
        ),
        # pipeline(model="google/vit-base-patch16-224"),
        # pipeline(model="t5-base", tokenizer="t5-base"),
        BigGAN.from_pretrained("biggan-deep-256"),
    )


classifier, translator, generator = load_model()


def classify(images: list):
    input_images = []
    for image_data in images:
        input_images.append(Image.open(BytesIO(base64.b64decode(image_data))))
    return classifier(input_images)


def translate(text: list):
    return translator(text)[0]["translation_text"]


def generate(text: list):
    # Prepare a input
    truncation = 0.4
    class_vector = one_hot_from_names(text, batch_size=1)
    noise_vector = truncated_noise_sample(truncation=truncation, batch_size=1)

    # All in tensors
    noise_vector = torch.from_numpy(noise_vector)
    class_vector = torch.from_numpy(class_vector)

    # If you have a GPU, put everything on cuda
    noise_vector = noise_vector.to("cpu")
    class_vector = class_vector.to("cpu")
    generator.to("cpu")

    # Generate an image
    with torch.no_grad():
        output = generator(noise_vector, class_vector, truncation)
    results = []
    for img in convert_to_images(output):
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        base64_img_str = base64.b64encode(buffered.getvalue()).decode()
        results.append(base64_img_str)
    return results


# https://huggingface.co/spaces/akhaliq/AnimeGANv2/blob/main/app.py
def load_anime_gan():
    return torch.hub.load(
        "AK391/animegan2-pytorch:main",
        "generator",
        pretrained=True,
        device="cpu",
        progress=False,
    ), torch.hub.load(
        "AK391/animegan2-pytorch:main",
        "face2paint",
        size=512,
        device="cpu",
        side_by_side=False,
    )


anime_gan_model, anime_gan_entrypoint = load_anime_gan()


def transfer(images: list):
    results = []
    for image_data in images:
        input_image = Image.open(BytesIO(base64.b64decode(image_data))).convert("RGB")
        result_img = anime_gan_entrypoint(anime_gan_model, input_image)
        buffered = BytesIO()
        result_img.save(buffered, format="JPEG")
        base64_img_str = base64.b64encode(buffered.getvalue()).decode()
        results.append(base64_img_str)
    return results


service = Server()
service.register(
    model_name="image-classifications",
    model=classify,
    metadata={"task": task.IMAGE_CLASSIFICATION},
    # metadata={"task": "invalid"},
)
service.register(
    model_name="image-classifications",
    model=classify,
    version_name="v1",
    metadata={"task": task.IMAGE_CLASSIFICATION},
)
service.register(
    model_name="t5",
    model=translate,
    version_name="v1",
    metadata={"task": task.TRANSLATION},
)
service.register(
    model_name="biggan",
    model=generate,
    version_name="v1",
    metadata={"task": task.TEXT_TO_IMAGE},
)
service.register(
    model_name="anime-gan",
    model=transfer,
    version_name="v1",
    metadata={
        "task": task.IMAGE_STYLE_TRANSFER,
        "display_name": "Anime GAN",
        "description": "This is anime GAN",
    },
)
