from fastapi import APIRouter, Depends

from src.api.dependencies.auth import get_current_superuser, AuthenticatedUser
from src.api.dependencies.services.user import UserServiceDep
from src.domain.schemas.user import UserReadSchema, UserUpdateSchema
from src.domain.models.user import User

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "",
    dependencies=[Depends(get_current_superuser)],
    response_model=list[UserReadSchema],
)
async def get_all_users(user_service: UserServiceDep,
                        offset: int = 0,
                        limit: int = 100) -> list[User]:
    return await user_service.get_all(offset=offset, limit=limit)


# NOTE: Важно, чтобы эти эндпоинты были зарегистрированы раньше, чем /{user_id}
@router.get("/me", response_model=UserReadSchema)
async def get_authenticated_user(user: AuthenticatedUser) -> User:
    return user


@router.put("/me", response_model=UserReadSchema)
async def update_authenticated_user(
        schema: UserUpdateSchema,
        user: AuthenticatedUser,
        user_service: UserServiceDep
) -> User:
    user = await user_service.update_by_id(schema, user.id)
    return user


@router.get("/{user_id}",
            dependencies=[Depends(get_current_superuser)],
            response_model=UserReadSchema)
async def get_user(
        user_id: int,
        user_service: UserServiceDep) -> User:
    user = await user_service.get_by_id(user_id)
    return user


@router.delete("/{user_id}",
               dependencies=[Depends(get_current_superuser)],
               response_model=UserReadSchema)
async def delete_user(
        user_id: int,
        user_service: UserServiceDep) -> User:
    user = await user_service.delete_by_id(user_id)
    return user
