from app.worker import start_worker

from uuid import UUID

from fastapi import FastAPI, HTTPException

from app.models import Job, JobCreate
from app.storage import jobs
from app.queue import job_queue

start_worker()
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Distributed Job System API"}

@app.post("/jobs", response_model=Job)
def create_job(job_data: JobCreate):
    job = Job(
        task=job_data.task,
        payload=job_data.payload,
    )

    jobs[job.id] = job
    job_queue.put(job.id)
    return job

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: UUID):

    job = jobs.get(job_id)

    if job is None:

        raise HTTPException(

            status_code=404,

            detail="Job not found",

        )

    return job

@app.get("/queue/size")
def get_queue_size():
    return {"size": job_queue.qsize()}