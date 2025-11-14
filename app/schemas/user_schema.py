from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    surname: str | None = Field(
        None,
        min_length=1,
        max_length=50
    )
    email: EmailStr = Field(
        ...,
        max_length=100,
    )
    points: int = Field(0, description="User's current point balance")


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