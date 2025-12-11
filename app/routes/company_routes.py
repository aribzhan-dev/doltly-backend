from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.core.auth_deps import get_current_user
from app.core.company_deps import is_company_owner

from app.schemas.company_schema import (
    CompanyCreate,
    CompanyLogin,
    AddEmployeeRequest,
    CompanyOut,
    EmployeeOut
)

from app.services.company_service import (
    create_company,
    company_login,
    add_employee_to_company,
    get_company_by_name,
    get_company_employees,
    get_user_companies,
    join_company_by_invite,
    promote_to_owner,
    get_company_by_id,
)

router = APIRouter(prefix="/company", tags=["Company"])


@router.post("/create", response_model=CompanyOut)
async def create_company_route(
    payload: CompanyCreate,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    return await create_company(session, owner_id=current_user, data=payload)



@router.post("/login")
async def company_login_route(
    payload: CompanyLogin,
    session: AsyncSession = Depends(get_session)
):
    return await company_login(session, payload)



@router.post("/{company_id}/add-employee")
async def add_employee_route(
    company_id: int,
    request: AddEmployeeRequest,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user),
    company = Depends(is_company_owner)
):
    return await add_employee_to_company(
        session, company_id, request.user_nick
    )


@router.get("/id/{company_id}/employees", response_model=list[EmployeeOut])
async def get_employees_by_id(
    company_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    return await get_company_employees(session, company_id)


@router.get("/name/{comp_name}/employees", response_model=list[EmployeeOut])
async def get_employees_by_name(
    comp_name: str,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    company = await get_company_by_name(session, comp_name)
    return company.employees



@router.get("/my", response_model=list[CompanyOut])
async def get_my_companies(
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    return await get_user_companies(session, current_user)


@router.post("/join/{invite_code}")
async def join_company_route(
    invite_code: str,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    return await join_company_by_invite(session, invite_code, current_user)



@router.post("/{company_id}/promote/{user_id}")
async def promote_to_owner_route(
    company_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: int = Depends(get_current_user),
    company = Depends(is_company_owner)
):
    return await promote_to_owner(session, company_id, user_id, current_user)