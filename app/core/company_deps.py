from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_session
from app.core.auth_deps import get_current_user
from app.models.company_model import Company


async def is_company_owner(
    company_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    stmt = select(Company).where(Company.id == company_id)
    result = await session.execute(stmt)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Company not found")

    if company.owner_id != current_user:
        raise HTTPException(403, "Access denied. You are not the company owner.")

    return company