import math


class SumProductModel:
    def predict(self, data):
        if hasattr(math, "prod"):
            return {"sum": sum(data), "product": math.prod(data)}
        else:
            # if python version < 3.8
            import operator
            from functools import reduce

            return {"sum": sum(data), "product": reduce(operator.mul, data, 1)}


model = SumProductModel()
inference_data = [
    {"request_data": [1, 2], "response_data": {"sum": 3, "product": 2}},
    {"request_data": [1, 2, 3], "response_data": {"sum": 6, "product": 6}},
    {"request_data": [1, 2, -3], "response_data": {"sum": 0, "product": -6}},
    {
        "request_data": [1, 2, 3, 4],
        "response_data": {"sum": 10, "product": 24},
    },
]
metadata = {
    "platform": "mac os",
    "inputs": [
        {
            "name": "integers",
            "datatype": "int64",
            "shape": [1],
            "data": [1, 2, 3],
        }
    ],
    "outputs": [
        {"name": "sum", "datatype": "int64", "shape": -1, "data": 6},
        {"name": "product", "datatype": "int64", "shape": -1, "data": 6},
    ],
}
