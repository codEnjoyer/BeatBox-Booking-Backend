from typing import Annotated

from fastapi import Depends

from src.domain.services.user import UserService


def get_user_service() -> UserService:
    return UserService()


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
