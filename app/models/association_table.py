from sqlalchemy import Table, Column, ForeignKey, Integer
from app.models.base import Base

user_task_association = Table(
    "user_task_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)