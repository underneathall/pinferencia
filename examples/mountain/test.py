import requests

response = requests.post(
    url="http://localhost:8000/v1/models/mountain/predict",
    json={"data": [1000, 2000, 3000]},
)
difference = response.json()["data"]
print(f"Difference between the highest and lowest is {difference}m.")
