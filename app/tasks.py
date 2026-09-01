def calculate_sum(payload: dict):
    return payload["a"] + payload["b"]

def divide(payload: dict):
    return payload["a"] / payload["b"]

TASKS = {
    "calculate_sum": calculate_sum,
    "divide": divide,
}