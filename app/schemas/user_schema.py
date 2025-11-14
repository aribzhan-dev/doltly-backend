from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(... ,max_length=50, min_length=1)
    surname: str | None = Field(None, max_length=50)
    email: EmailStr = Field(
        ...,
        max_length=100,
        pattern=r"^[\w.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    point: int = Field(..., description="Point")


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$",
        description="Password must contain uppercase, lowercase, digit and special character",
    )

class User(UserBase):
    id: int
    model_config = {"from_attributes": True}