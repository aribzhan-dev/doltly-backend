from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Task(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    task_desc: Mapped[str] = mapped_column(String(500))
    deadline: Mapped[datetime] = mapped_column(nullable=False)
    who_must_do_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_users: Mapped[list["User"]] = relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}: {self.task_desc}>"