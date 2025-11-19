from typing import List

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.user_schema import UserCreate, UserUpdate, User, UserBase, LoginSchema
from app.services.user_service import (
    get_user as get_user_service,
    get_user_by_email as get_user_by_email_service,
    create_user as create_user_service,
    get_user_by_id as get_user_by_id_service,
    update_user as update_user_service,
)
from app.services.auth_service import login_user as login_user_service
from app.core.db import get_session



router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_route(
        payload: UserCreate,
        session: AsyncSession = Depends(get_session),
):
    return await create_user_service(session, payload)



@router.get("/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users_routes(
        session: AsyncSession = Depends(get_session),
):
    return await get_user_service(session)


@router.get("/{user_id}", response_model=User)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await get_user_by_id_service(session, user_id)


@router.put("/{user_id}", response_model=User)
async def update_user(
        user_id: int,
        payload: UserUpdate,
        session: AsyncSession = Depends(get_session),
):
    return await update_user_service(session, user_id, payload)





