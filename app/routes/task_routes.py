from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task_schema import TaskCreate, Task
from app.services.task_service import create_task
from app.core.db import get_session




router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.post("/", response_model=Task,  status_code=status.HTTP_201_CREATED)