from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_session
from app.core.auth_deps import get_current_user
from app.models.company_model import Company, company_employers


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


    if company.owner_id == current_user:
        return company

    stmt = select(company_employers.c.role).where(
        company_employers.c.company_id == company_id,
        company_employers.c.user_id == current_user
    )
    result = await session.execute(stmt)
    row = result.first()

    if row and row[0] == "owner":
        return company

    raise HTTPException(403, "You are not an owner of this company")