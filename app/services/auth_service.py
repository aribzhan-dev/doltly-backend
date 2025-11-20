from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User
from app.core.auth_utils import create_access_token, create_refresh_token
import bcrypt

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
        "token_type": "bearer"
    }