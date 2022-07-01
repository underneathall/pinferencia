from typing import List

from pinferencia import Server


def stat(data: List[float]) -> float:
    return sum(data)


service = Server()
service.register(
    model_name="stat",
    model=stat,
    metadata={"display_name": "Awesome Model"},
)
