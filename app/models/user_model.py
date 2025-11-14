from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.association_table import user_task_association

class User(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0)

    tasks: Mapped[List["Task"]] = relationship(
        secondary=user_task_association,
        back_populates="users"
    )

    def __repr__(self):
        return f"<User {self.name} {self.surname}>"