from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task_schema import TaskCreate, Task
from app.services.task_service import create_task, get_tasks, get_task_by_id, get_task_by_title, get_task_by_deadline
from app.core.db import get_session




router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.post("/", response_model=Task,  status_code=status.HTTP_201_CREATED)
async def create_task(
        payload: TaskCreate,
        session: AsyncSession = Depends(get_session),
):
    return await create_task(session, payload)


@router.get("/", response_model=list[Task], status_code=status.HTTP_200_OK)
async def get_tasks(
        session: AsyncSession = Depends(get_session),
):
    return await get_tasks(session)


@router.get("/{task_id}", response_model=Task)
async def get_task_by_id(
        task_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await get_task_by_id(session, task_id)

