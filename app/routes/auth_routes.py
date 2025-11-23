from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import login_user
from app.core.auth_utils import decode_refresh_token, create_access_token, create_refresh_token
from app.core.db import get_session
from app.schemas.user_schema import UserCreate, LoginSchema, TokenResponse
from app.services.auth_service import create_user as create_user_service
from starlette import status


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(
        payload: UserCreate,
        session: AsyncSession = Depends(get_session),
):
    return await create_user_service(session, payload)


@router.post("/login")
async def login_route(payload: LoginSchema, session: AsyncSession = Depends(get_session)):
    return await login_user(session, payload.email, payload.password)


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    new_access = create_access_token({"user_id": payload["user_id"]})
    new_refresh = create_refresh_token({"user_id": payload["user_id"]})
    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "Bearer"
    }