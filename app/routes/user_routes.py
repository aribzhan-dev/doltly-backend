from typing import List

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.auth_deps import get_current_user
from app.schemas.user_schema import UserCreate, UserUpdate, User, UserBase, LoginSchema
from app.services.user_service import (
    get_user as get_user_service,
    get_user_by_email as get_user_by_email_service,
    get_user_by_id as get_user_by_id_service,
    update_user as update_user_service,
)
from app.services.auth_service import login_user as login_user_service
from app.core.db import get_session



router = APIRouter(prefix="/users", tags=["Users"])



@router.get("api/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users_routes(
        session: AsyncSession = Depends(get_session),
        current_user: int = Depends(get_current_user)
):
    return await get_user_service(session)



@router.get("/me", response_model=User)
async def get_me(
        session: AsyncSession = Depends(get_session),
        user_id: int = Depends(get_current_user)
):
    user = await get_user_by_id_service(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user





@router.get("/{user_id}", response_model=User)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: int = Depends(get_current_user)
):
    return await get_user_by_id_service(session, user_id)


@router.put("/{user_id}", response_model=User)
async def update_user(
        user_id: int,
        payload: UserUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: int = Depends(get_current_user)
):
    return await update_user_service(session, user_id, payload)










