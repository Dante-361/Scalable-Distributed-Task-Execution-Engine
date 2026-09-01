from queue import Queue
from uuid import UUID

from app.models import Job

job_queue: Queue[UUID] = Queue()