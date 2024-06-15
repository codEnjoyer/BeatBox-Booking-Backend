from fastapi import APIRouter

from src.api.v1.dependencies.auth import (AuthenticatedUser,
                                          AuthenticatedSuperuser)
from src.api.v1.dependencies.services import UserServiceDep
from src.api.v1.dependencies.types import QueryLimit, QueryOffset
from src.api.v1.dependencies.user import ValidUserIdDep
from src.domain.schemas.user import UserRead, UserUpdate
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
async def get_authenticated_user(user: AuthenticatedUser) -> User:
    return user


@router.put("/me", response_model=UserRead)
async def update_authenticated_user(
    schema: UserUpdate,
    user: AuthenticatedUser,
    user_service: UserServiceDep,
) -> User:
    user = await user_service.update_by_id(schema, user.id)
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


@router.delete("/{user_id}")
async def delete_user(
    user: ValidUserIdDep,
    user_service: UserServiceDep,
    _: AuthenticatedSuperuser,
) -> None:
    await user_service.delete_by_id(user.id)
