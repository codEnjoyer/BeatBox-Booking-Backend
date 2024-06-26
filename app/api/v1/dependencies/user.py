from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from api.v1.dependencies.services import UserServiceDep
from api.v1.dependencies.types import PathIntID
from exceptions.user import UserNotFoundException
from models import User


async def valid_user_id(
    user_id: PathIntID, user_service: UserServiceDep
) -> User:
    try:
        user = await user_service.get_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    return user


ValidUserIdDep = Annotated[User, Depends(valid_user_id)]
