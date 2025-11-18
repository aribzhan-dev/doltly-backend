from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task_schema import TaskCreate, Task, TaskStatus
from app.services.task_service import (
    create_task as create_task_service,
    get_tasks as get_tasks_service,
    get_task_by_id as get_task_by_id_service,
    update_task_status as update_task_status_service
)
from app.core.db import get_session


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
        payload: TaskCreate,
        session: AsyncSession = Depends(get_session),
):
    return await create_task_service(session, payload)


@router.get("/", response_model=list[Task], status_code=status.HTTP_200_OK)
async def get_tasks(
        session: AsyncSession = Depends(get_session),
):
    return await get_tasks_service(session)


@router.get("/{task_id}", response_model=Task)
async def get_task_by_id(
        task_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await get_task_by_id_service(session, task_id)


@router.put("/{task_id}", response_model=Task)
async def update_task_status_route(
        task_id: int,
        task_status: TaskStatus,
        session: AsyncSession = Depends(get_session),
):
    return await update_task_status_service(session, task_id, task_status)