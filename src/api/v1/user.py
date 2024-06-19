from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.v1.dependencies.auth import (
    AuthenticatedUser,
    AuthenticatedSuperuser,
)
from src.api.v1.dependencies.services import UserServiceDep
from src.api.v1.dependencies.types import QueryLimit, QueryOffset
from src.api.v1.dependencies.user import ValidUserIdDep
from src.domain.exceptions.user import (
    EmailAlreadyTakenException,
    NicknameAlreadyTakenException,
)
from src.domain.schemas.user import UserRead, UserUpdate, UserPasswordUpdate
from src.domain.models.user import User

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "",
    response_model=list[UserRead],
)
async def get_all_users(
    user_service: UserServiceDep,
    _: AuthenticatedSuperuser,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[User]:
    return await user_service.get_all(offset=offset, limit=limit)


# NOTE: Важно, чтобы me-эндпоинты были зарегистрированы раньше, чем /{user_id}
@router.get("/me", response_model=UserRead)
async def get_my_info(user: AuthenticatedUser) -> User:
    return user


@router.post("/me", response_model=UserRead)
async def change_my_password(
    schema: UserPasswordUpdate,
    user: AuthenticatedUser,
    user_service: UserServiceDep,
) -> User:
    if not user_service.is_password_valid(
        schema.old_password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong old password"
        )
    return await user_service.update_password(user, schema.new_password)


@router.put("/me", response_model=UserRead)
async def update_my_info(
    schema: UserUpdate,
    user: AuthenticatedUser,
    user_service: UserServiceDep,
) -> User:
    try:
        user = await user_service.update(user, schema)
    except (EmailAlreadyTakenException, NicknameAlreadyTakenException) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return user


@router.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user(
    user: ValidUserIdDep,
    user_service: UserServiceDep,
    _: AuthenticatedSuperuser,
) -> User:
    return await user_service.get_by_id(user.id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user: ValidUserIdDep,
    user_service: UserServiceDep,
    _: AuthenticatedSuperuser,
) -> None:
    await user_service.delete_by_id(user.id)
