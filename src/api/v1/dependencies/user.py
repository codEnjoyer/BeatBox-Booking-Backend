from typing import Annotated

from fastapi import HTTPException, Depends
from pydantic import PositiveInt
from starlette import status

from src.api.v1.dependencies.services import UserServiceDep
from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import User


async def valid_user_id(
    user_id: PositiveInt, user_service: UserServiceDep
) -> User:
    try:
        user = await user_service.get_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return user


ValidUserIdDep = Annotated[User, Depends(valid_user_id)]
