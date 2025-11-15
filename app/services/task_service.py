from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate
from datetime import datetime

async def create_task(session: AsyncSession, data: TaskCreate):
    stmt = select(User).where(User.id.in_(data.user_ids))
    result = await session.execute(stmt)
    users = result.scalars().all()

    if len(users) != len(data.user_ids):
        raise ValueError("Some user IDs not found")


    task = Task(
        title=data.title,
        task_desc=data.task_desc,
        deadline=data.deadline,
    )

    task.users = users

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task



async def get_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task).order_by(Task.id)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return list(tasks)


async def get_task_by_id(session: AsyncSession, task_id: int) -> Task:
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().one_or_none()
    if not task:
        raise ValueError("Task not found")
    return task

async def get_task_by_title(session: AsyncSession, title: str) -> Task:
    stmt = select(Task).where(Task.title == title)
    result = await session.execute(stmt)
    task = result.scalars().all()


async def get_task_by_deadline(session: AsyncSession, deadline: datetime) -> Task:
    stmt = select(Task).where(Task.deadline == deadline)
    result = await session.execute(stmt)
    task = result.scalars().one_or_none()
    if not task:
        raise ValueError("Task not found")
    return task



