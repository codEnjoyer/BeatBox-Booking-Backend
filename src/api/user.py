from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies.auth import (
    get_user_by_id,
    AuthenticatedUser,
    get_current_superuser,
)
from src.domain.db import get_async_session
from src.domain.schemas.user import UserReadSchema
from src.domain.models.user import User

router = APIRouter(prefix="/users", tags=["User"])


# services
@router.get(
    "/",
    dependencies=[Depends(get_current_superuser)],
    response_model=list[UserReadSchema],
)
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}")
async def read_user(
    user_id: int,
    active_user: AuthenticatedUser,
    session: AsyncSession = Depends(get_async_session),
) -> UserReadSchema:
    user = await get_user_by_id(user_id, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.id != active_user.id and not active_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this user",
        )

    return UserReadSchema(id=user.id, email=user.email)
