from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.core.auth_deps import get_current_user
from app.models.company_model import company_employers

async def is_company_owner(
    company_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    stmt = (
        select(company_employers.c.role)
        .where(company_employers.c.company_id == company_id)
        .where(company_employers.c.user_id == current_user)
    )
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if role != "owner":
        raise HTTPException(403, "Only owner can access this resource")

    return True