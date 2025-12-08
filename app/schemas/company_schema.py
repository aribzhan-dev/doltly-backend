from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional

class CompanyCreate(BaseModel):
    name: str = Field(..., max_length=100, min_length=2, description="Company name")
    login: str = Field(..., max_length=100, min_length=2, description="Company login")
    password: str = Field(..., max_length=100, min_length=2, description="Company password")



class CompanyLogin(BaseModel):
    login: str = Field(..., max_length=100, min_length=2, description="Company login")
    password: str = Field(..., max_length=100, min_length=2, description="Company password")


class EmployeeOut(BaseModel):
    id: int
    name: str = Field(..., max_length=100, min_length=2, description="User name")
    surname: str = Field(..., max_length=100, min_length=2, description="User surname")

    class Config:
        orm_mode = True


class CompanyOut(BaseModel):
    id: int
    name: str = Field(..., max_length=100, min_length=2, description="Company name")
    login: str = Field(..., max_length=100, min_length=2, description="Company login")
    owner_id: Optional[int]
    employees: List[EmployeeOut] = []

    model_config = ConfigDict(from_attributes=True)


class AddEmployeeRequest(BaseModel):
    user_id: int