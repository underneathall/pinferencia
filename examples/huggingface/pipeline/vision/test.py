import requests

response = requests.post(
    url="http://localhost:8000/v1/models/vision/predict",
    json={
        "data": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"  # noqa
    },
)
print("Prediction:", response.json()["data"])
