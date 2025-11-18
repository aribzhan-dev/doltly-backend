from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user_model import User
from fastapi import HTTPException
from app.schemas.user_schema import User as UserSchema, UserCreate, UserBase
import bcrypt





async def create_user(session: AsyncSession, data: UserCreate):
    stmt = select(User).where(User.email == data.email)
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
        name=data.name,
        surname=data.surname,
        email=data.email,
        password=hashed_password,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def login_user(session: AsyncSession, email: str, password: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )

    return user


