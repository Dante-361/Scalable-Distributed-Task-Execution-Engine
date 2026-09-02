import subprocess
import time
import requests


API_URL = "http://127.0.0.1:8000/jobs"

NUM_JOBS = 6
TASK_SECONDS = 5


def submit_jobs():
    job_ids = []

    for _ in range(NUM_JOBS):
        response = requests.post(
            API_URL,
            json={
                "task": "slow_task",
                "payload": {
                    "seconds": TASK_SECONDS
                }
            }
        )

        response.raise_for_status()
        job_ids.append(response.json()["id"])

    return job_ids


def wait_for_jobs(job_ids):
    while True:
        completed = 0

        for job_id in job_ids:
            response = requests.get(f"{API_URL}/{job_id}")
            response.raise_for_status()

            status = response.json()["status"]

            if status in ["completed", "failed"]:
                completed += 1

        if completed == len(job_ids):
            return

        time.sleep(0.1)


def benchmark():
    print(f"Submitting {NUM_JOBS} jobs...")
    print(f"Each job sleeps for {TASK_SECONDS} seconds.\n")

    start = time.perf_counter()

    job_ids = submit_jobs()

    wait_for_jobs(job_ids)

    elapsed = time.perf_counter() - start

    print(f"Completed {NUM_JOBS} jobs in {elapsed:.2f} seconds")


if __name__ == "__main__":
    benchmark()