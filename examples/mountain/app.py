from typing import List

from pinferencia import Server


def calc(data: List[int]) -> int:
    highest = max(data)
    lowest = min(data)
    return highest - lowest


service = Server()
service.register(model_name="mountain", model=calc)
