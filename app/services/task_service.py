from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskStatusUpdate, TaskStatus
from datetime import datetime
from fastapi import HTTPException

async def create_task(session: AsyncSession, data: TaskCreate):
    stmt = select(User).where(User.id.in_(data.user_ids))
    result = await session.execute(stmt)
    users = result.scalars().all()

    if len(users) != len(data.user_ids):
        raise HTTPException(status_code=400, detail="Some user IDs not found")

    task = Task(
        title=data.title,
        task_desc=data.task_desc,
        deadline=data.deadline,
        point=data.point
    )

    task.users = users

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task



async def get_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task).order_by(Task.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_task_by_id(session: AsyncSession, task_id: int) -> Task:
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

async def get_task_by_title(session: AsyncSession, title: str) -> list[Task]:
    stmt = select(Task).where(Task.title == title)
    result = await session.execute(stmt)
    return result.scalars().all()




async def get_task_by_deadline(session: AsyncSession, deadline: datetime):
    stmt = select(Task).where(func.date(Task.deadline) == deadline.date())
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_task_status(session: AsyncSession, task_id: int, new_status: TaskStatus):
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = new_status

    if new_status == TaskStatus.completed:
        for user in task.users:
            user.points += task.point

    await session.commit()
    await session.refresh(task)

    return task



