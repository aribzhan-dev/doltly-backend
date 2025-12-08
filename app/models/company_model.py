from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import Base

company_employers = Table(
    "company_employers",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("company.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

class Company(Base):
    name = Column(String(150), nullable=False)
    login = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    owner = relationship("User")

    employees = relationship(
        "User",
        secondary=company_employers,
        back_populates="companies"
    )

    tasks = relationship("Task", back_populates="company")