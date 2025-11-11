from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from app.models.base import Base
from sqlalchemy import String
from app.models.task_model import Task


class User(Base):
    name : Mapped[str] = mapped_column(String(50), nullable=False)
    surname : Mapped[str] = mapped_column(String(50) ,nullable=False)
    email : Mapped[str] = mapped_column(String(50) ,unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(50) ,nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="assigned_user", cascade="all, delete")

    def __repr__(self):
        return f"<User {self.name}: {self.surname}>"