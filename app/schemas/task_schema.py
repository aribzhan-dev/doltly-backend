from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.models.task_model import TaskStatus

KZ_TZ=ZoneInfo("Asia/Almaty")



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
    user_ids: list[int] = Field(default_factory=list, description="List of user ids")

class TaskCreate(TaskBase):
    @field_validator("deadline", mode="before")
    def validate_deadline(cls, value):
        if value < datetime.now(KZ_TZ):
            raise ValueError("Deadline must be a future date")
        return value



class Task(TaskBase):
    id: int
    status: TaskStatus
    users: list[int] = []
    model_config = {"from_attributes": True}

