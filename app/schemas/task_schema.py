from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.models.task_model import TaskStatus
from app.models.user_model import User
from app.schemas.user_schema import UserShort


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
    point: int = Field(0, description="Enter a point for the task")
    user_ids: list[int] = Field(default_factory=list, description="List of user ids")



class TaskStatusUpdate(BaseModel):
    task_status: TaskStatus



class TaskCreate(TaskBase):
    @field_validator("deadline")
    def validate_deadline(cls, value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=KZ_TZ)
        if value < datetime.now(KZ_TZ):
            raise ValueError("Deadline must be a future date")
        return value


class Task(TaskBase):
    id: int
    status: TaskStatus
    users: list[UserShort]
    model_config = {"from_attributes": True}

