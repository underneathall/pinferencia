from tests.models.json_model.model import inference_data as json_data
from tests.models.sum_product_model import inference_data as sum_prod_data

json_inference_data = [
    {
        "request": {"instances": d["request_data"]},
        "response": {"predictions": d["response_data"]},
    }
    for d in json_data
]

sum_prod_inference_data = [
    {
        "request": {"instances": d["request_data"]},
        "response": {"predictions": d["response_data"]},
    }
    for d in sum_prod_data
]
