from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import LoginSchema
from app.services.auth_service import login_user
from app.core.auth_utils import decode_refresh_token, create_access_token
from app.core.db import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login_route(payload: LoginSchema, session: AsyncSession = Depends(get_session)):
    return await login_user(session, payload.email, payload.password)


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    new_access = create_access_token({"user_id": payload["user_id"]})
    return {"access_token": new_access, "token_type": "bearer"}