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


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="Password must contain uppercase, lowercase, digit and special character",
    )


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    password: str | None = None

class LoginSchema(BaseModel):
    email: EmailStr = Field(
        ...,
        max_length=50
    )
    password: str = Field(
        min_length=8,
        max_length=50
    )

class UserShort(BaseModel):
    id: int
    name: str
    surname: str

    model_config = {"from_attributes": True}



class User(UserBase):
    id: int
    model_config = {"from_attributes": True}