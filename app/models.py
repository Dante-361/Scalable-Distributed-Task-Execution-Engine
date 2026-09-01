from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"

class JobCreate(BaseModel):
    task: str
    payload: dict = Field(default_factory=dict)

class Job(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    task: str
    payload: dict
    status: JobStatus = JobStatus.QUEUED
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    result: object | None = None 