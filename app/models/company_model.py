from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class CompanyRole(str, enum.Enum):
    owner = "owner"
    employee = "employee"

company_employers = Table(
    "company_employers",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role", Enum(CompanyRole), nullable=False, default=CompanyRole.employee)
)

class Company(Base):
    __tablename__ = "companies"
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    name = Column(String(150), nullable=False)
    login = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    invite_code = Column(String(255), nullable=False, unique=True)

    owner = relationship("User")
    employees = relationship(
        "User",
        secondary=company_employers,
        back_populates="companies",
        lazy="selectin"
    )
    tasks = relationship("Task", back_populates="company", lazy="selectin")

    def __repr__(self) -> str:
        return f"Company {self.name}"
