from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone

class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Title of the task"
    )
    task_desc: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Detailed description"
    )
    deadline: datetime = Field(...)
    executor_id: int = Field(
        ...,
        description="User ID who must complete the task"
    )

class TaskCreate(TaskBase):
    @field_validator("deadline")
    def validate_deadline(cls, value):
        if value < datetime.now(timezone.utc):
            raise ValueError("Deadline must be a future date")
        return value

class Task(TaskBase):
    id: int
    model_config = {"from_attributes": True}

