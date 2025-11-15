from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate

async def create_task(session: AsyncSession, data: TaskCreate):
    stmt = select(User).where(User.id.in_(data.user_ids))
    result = await session.execute(stmt)
    user = result.scalars().all()

    if len(user) != len(data.user_ids):
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

