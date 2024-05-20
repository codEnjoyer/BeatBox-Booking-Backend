from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi_login import LoginManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.db import async_session_maker
from src.domain.models import User, Employee
from src.settings import settings

manager = LoginManager(settings.secret_auth_token, token_url="/auth/token")


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    stmt = select(User)
    stmt = stmt.filter_by(email=email)
    result = await session.execute(stmt)
    return result.unique().scalar_one()


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    stmt = select(User)
    stmt = stmt.filter_by(id=user_id)
    result = await session.execute(stmt)
    return result.unique().scalar_one()


@manager.user_loader()
async def get_user(name: str) -> User:
    """
    Raises:
        `LoginManager.not_authenticated_exception`: If the user is not found
    """
    async with async_session_maker() as db:
        return await get_user_by_email(name, db)


# Для читаемости при прописывании в dependencies эндпоинтов
get_current_user = manager

AuthenticatedUser = Annotated[User, Depends(manager)]


async def get_current_user_employee(user: AuthenticatedUser) -> Employee:
    employee: Employee | None = user.employee
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    return employee


AuthenticatedEmployee = Annotated[Employee, Depends(get_current_user_employee)]


async def get_current_superuser(user: AuthenticatedUser) -> User:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    return user


AuthenticatedSuperuser = Annotated[User, Depends(get_current_superuser)]
