from app.schemas.task_schema import TaskCreate, Task, TaskStatusUpdate
from app.services.task_service import (
    create_task as create_task_service,
    get_tasks as get_tasks_service,
    get_task_by_id as get_task_by_id_service,
    update_task_status as update_task_status_service
)
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth_deps import get_current_user
from app.core.db import get_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[Task])
async def get_tasks_route(
        type: str | None = None,
        session: AsyncSession = Depends(get_session),
        current_user: int = Depends(get_current_user)
):
    return await get_tasks_service(session, type, current_user)


@router.get("/{task_id}", response_model=Task)
async def get_task_by_id(
        task_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: int = Depends(get_current_user)
):
    return await get_task_by_id_service(session, task_id)


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
        payload: TaskCreate,
        session: AsyncSession = Depends(get_session),
        current_user: int = Depends(get_current_user)
):
    return await create_task_service(session, payload)


@router.put("/{task_id}", response_model=Task)
async def update_task_status_route(
        task_id: int,
        payload: TaskStatusUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: int = Depends(get_current_user)
):
    return await update_task_status_service(session, task_id, payload.task_status)
