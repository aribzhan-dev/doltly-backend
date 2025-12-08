from datetime import datetime
from enum import Enum
from typing import List
from sqlalchemy import String, Enum as SqlEnum, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.association_table import user_task_association

class TaskStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class Task(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    task_desc: Mapped[str | None] = mapped_column(String(500), nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus),
        default=TaskStatus.not_started,
        nullable=False,
    )

    point: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    users: Mapped[List["User"]] = relationship(
        secondary=user_task_association,
        back_populates="tasks"
    )
    company_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("company.id", ondelete="SET NULL"),
        nullable=True
    )
    company = relationship("Company", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task {self.title}>"