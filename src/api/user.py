from fastapi import APIRouter, Depends

from src.api.dependencies.auth import get_current_superuser, AuthenticatedUser
from src.api.dependencies.services import UserServiceDep
from src.api.dependencies.types import QueryLimit, QueryOffset
from src.domain.schemas.user import UserRead, UserUpdate
from src.domain.models.user import User

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "",
    dependencies=[Depends(get_current_superuser)],
    response_model=list[UserRead],
)
async def get_all_users(
    user_service: UserServiceDep,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[User]:
    return await user_service.get_all(offset=offset, limit=limit)


# NOTE: Важно, чтобы эти эндпоинты были зарегистрированы раньше, чем /{user_id}
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
    dependencies=[Depends(get_current_superuser)],
    response_model=UserRead,
)
async def get_user(user_id: int, user_service: UserServiceDep) -> User:
    user = await user_service.get_by_id(user_id)
    return user


@router.delete("/{user_id}", dependencies=[Depends(get_current_superuser)])
async def delete_user(user_id: int, user_service: UserServiceDep) -> None:
    await user_service.delete_by_id(user_id)
