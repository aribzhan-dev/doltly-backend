from datetime import datetime
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column,relationship
from app.models.base import Base
from app.models.user_model import User

class Task(Base):
    title : Mapped[str] = mapped_column()
    task_desc : Mapped[str] = mapped_column()
    deadline : Mapped[datetime] = mapped_column()
    who_must_do : Mapped[int] = mapped_column(foreign_key='user.id', ondelete='CASCADE', nullable=False)
    assigned_user : Mapped[User] = relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}:{self.task_desc}>"
