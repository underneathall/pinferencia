from typing import List

from pinferencia import Server


def stat(data: List[float]) -> dict:
    return {
        "mean": sum(data) / len(data),
        "max": max(data),
        "min": min(data),
    }


service = Server()
service.register(model_name="stat", model=stat, metadata={"task": "Stat"})
