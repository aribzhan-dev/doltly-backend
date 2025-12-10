from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    nickname: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
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
    nickname: str | None = None
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
    nickname: str
    name: str
    surname: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str



class User(UserBase):
    id: int
    model_config = {"from_attributes": True}