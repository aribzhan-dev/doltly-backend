from jose import jwt, JWTError
from fastapi import HTTPException
from app.core.auth_utils import create_access_token, create_refresh_token
import bcrypt
from app.models.user_model import User
from sqlalchemy import select


async def login_user(session, email: str, password: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(404, "User not found")

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise HTTPException(400, "Incorrect password")

    payload = {"user_id": user.id, "email": user.email}

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }