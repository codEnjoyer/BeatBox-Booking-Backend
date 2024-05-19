from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi_login import LoginManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.db import async_session_maker
from src.domain.models import User
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


CurrentUserDep = Annotated[User, Depends(manager)]


async def get_current_employee(current_user: CurrentUserDep) -> User:
    if current_user.employee is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not an employee")
    return current_user


CurrentEmployeeDep = Annotated[User, Depends(get_current_employee)]


async def get_current_superuser(current_user: CurrentUserDep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not a superuser")
    return current_user


CurrentSuperuserDep = Annotated[User, Depends(get_current_superuser)]
