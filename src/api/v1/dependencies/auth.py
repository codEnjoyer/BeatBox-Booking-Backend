from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi_login import LoginManager

from src.domain.db import async_session_maker
from src.domain.models import User, Employee
from src.domain.services.user import UserService
from src.settings import settings

manager = LoginManager(settings.secret_auth_token, token_url="/auth/token")


@manager.user_loader()
async def get_user(email: str) -> User:
    """
    Raises:
        `LoginManager.not_authenticated_exception`: If the user is not found
    """
    async with async_session_maker() as db:
        return await UserService.get_user_by_email(email, db)


# Для читаемости при прописывании в dependencies эндпоинтов
get_current_user = manager

AuthenticatedUser = Annotated[User, Depends(get_current_user)]


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
