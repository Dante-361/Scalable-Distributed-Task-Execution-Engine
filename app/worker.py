import threading

from app.queue import job_queue
from app.storage import jobs
from app.models import JobStatus


def run_worker():
    print("Worker started")

    while True:
        job_id = job_queue.get()

        job = jobs.get(job_id)

        if job is None:
            job_queue.task_done()
            continue

        print(f"Processing job {job.id}")

        job.status = JobStatus.RUNNING
        job.result = {
            "message": f"Executed task: {job.task}"
        }
        job.status = JobStatus.COMPLETED

        print(f"Completed job {job.id}")

        job_queue.task_done()


def start_worker():
    thread = threading.Thread(
        target=run_worker,
        daemon=True
    )
    thread.start()