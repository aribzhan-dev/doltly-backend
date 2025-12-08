from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
import bcrypt
import secrets
from app.models.company_model import Company, company_employers
from app.models.user_model import User
from app.schemas.company_schema import CompanyCreate, CompanyLogin
from app.core.auth_utils import create_access_token, create_refresh_token



async def create_company(session: AsyncSession, owner_id: int, data: CompanyCreate):
    stmt = select(Company).where(Company.login == data.login)
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(400, "Login already exists.")

    hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    invite_code = secrets.token_hex(4)

    company = Company(
        name=data.name,
        login=data.login.lower(),
        password=hashed_pw,
        invite_code=invite_code,
        owner_id=owner_id
    )

    session.add(company)
    await session.commit()
    await session.refresh(company)

    return company



async def get_company_by_id(session: AsyncSession, company_id: int):
    stmt = select(Company).where(Company.id == company_id)
    result = await session.execute(stmt)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Company not found")

    return company



async def company_login(session: AsyncSession, data: CompanyLogin):
    stmt = select(Company).where(Company.login == data.login.lower())
    result = await session.execute(stmt)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(400, "Invalid login or password")

    if not bcrypt.checkpw(data.password.encode(), company.password.encode()):
        raise HTTPException(400, "Invalid login or password")

    access = create_access_token({"company_id": company.id})
    refresh = create_refresh_token({"company_id": company.id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer",
        "company_id": company.id,
    }



async def add_employee_to_company(session: AsyncSession, company_id: int, user_nick: str):
    company = await get_company_by_id(session, company_id)


    stmt = select(User).where(User.nickname == user_nick.lower())
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(404, "User not found")


    if user in company.employees:
        raise HTTPException(400, "User already in company")

    company.employees.append(user)

    await session.commit()
    await session.refresh(company)

    return {"message": "Employee added", "company_id": company.id, "user_nick": user.nickname}



async def get_company_employees(session: AsyncSession, company_id: int):
    company = await get_company_by_id(session, company_id)
    return company.employees



async def get_user_companies(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(404, "User not found")

    return user.companies



async def join_company_by_invite(session: AsyncSession, invite_code: str, user_id: int):
    stmt = select(Company).where(Company.invite_code == invite_code)
    result = await session.execute(stmt)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Invalid invite code")

    stmt = select(User).where(User.id == user_id)
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()

    if not user:
        raise HTTPException(404, "User not found")

    if user in company.employees:
        raise HTTPException(400, "User already joined this company")

    company.employees.append(user)

    await session.commit()
    await session.refresh(company)

    return {"message": "Successfully joined", "company_id": company.id}