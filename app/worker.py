import threading

from app.queue import job_queue
from app.storage import jobs
from app.models import JobStatus
from app.tasks import TASKS


def run_worker(worker_id):
    while True:
        job_id = job_queue.get()

        try:
            job = jobs.get(job_id)

            if job is None:
                continue

            print(f"Worker {worker_id} Processing job {job.id}")

            job.status = JobStatus.RUNNING

            try:
                task_function = TASKS.get(job.task)

                if task_function is None:
                    raise ValueError(f"Unknown task: {job.task}")

                job.result = task_function(job.payload)
                job.status = JobStatus.COMPLETED

                print(f"Worker {worker_id} Completed job {job.id}")

            except Exception as error:
                job.status = JobStatus.FAILED
                job.error = str(error)

                print(f"Failed job {job.id}: {error} ")

        finally:
            job_queue.task_done()


def start_workers(num_workers: int = 1):

    for i in range(num_workers):
        thread = threading.Thread(
            target=run_worker,
            args = (i + 1,),
            daemon=True
        )
        thread.start()
        print(f"Worker {i + 1} started")