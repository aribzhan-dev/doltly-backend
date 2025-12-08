from app.core.auth_utils import create_access_token, create_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate
from app.models.user_model import User
from fastapi import HTTPException
from sqlalchemy import select
import bcrypt


async def create_user(session: AsyncSession, data: UserCreate):
    stmt = select(User).where(User.nickname == data.nickname)
    if (await session.execute(stmt)).scalar_one_or_none():
        raise HTTPException(400, "Nickname already exists")
    result = await session.execute(stmt)
    existing_user = result.scalars().one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    byte_pass = data.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(byte_pass, salt).decode("utf-8")

    user = User(
        nickname=data.nickname.lower(),
        name=data.name,
        surname=data.surname,
        email=data.email,
        password=hashed_password,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    access = create_access_token({"user_id": user.id})
    refresh = create_refresh_token({"user_id": user.id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }


async def login_user(session: AsyncSession, email: str, password: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(404, "User not found")

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(400, "Incorrect password")

    access = create_access_token({"user_id": user.id})
    refresh = create_refresh_token({"user_id": user.id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }
