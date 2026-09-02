import time

def calculate_sum(payload: dict):
    return payload["a"] + payload["b"]

def divide(payload: dict):
    return payload["a"] / payload["b"]

def slow_task(payload: dict):
    time.sleep(payload.get("seconds", 2))
    return f"Slept for {payload.get('seconds', 2)} seconds"
    
               

TASKS = {
    "calculate_sum": calculate_sum,
    "divide": divide,
    "slow_task": slow_task,
}