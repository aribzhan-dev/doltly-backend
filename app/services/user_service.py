from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user_model import User
from fastapi import HTTPException
from app.schemas.user_schema import User as UserSchema, UserCreate, UserBase, UserUpdate
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

async def get_user(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user_by_email(session: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()


async def update_user(session: AsyncSession, user_id: int, data:UserUpdate):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    existing_user = result.scalars().one_or_none()

    if not existing_user:
        raise HTTPException(404, detail="User not found")

    if data.email:
        raise HTTPException(400, "Email cannot be updated")

    if data.password:
        byte_pass = data.password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(byte_pass, salt).decode("utf-8")
        existing_user.password = hashed_password

    if data.name:
        existing_user.name = data.name

    if data.surname:
        existing_user.surname = data.surname

    await session.commit()
    await session.refresh(existing_user)
    return existing_user




