from tests.models.json_model.model import inference_data as data

inference_data = [
    {
        "request": {"data": d["request_data"]},
        "response": {"data": d["response_data"]},
    }
    for d in data
]
