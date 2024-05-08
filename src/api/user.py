from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies.auth import get_user_by_name, CurrentUser
from src.domain.db import get_async_session
from src.domain.schemas.user import UserReadSchema
from src.domain.models.user import User

router = APIRouter(prefix="/user")


# services
@router.get("/", response_model=list[UserReadSchema])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{username}")
async def read_user(username: str,
                    active_user: CurrentUser,
                    session: AsyncSession = Depends(get_async_session)) \
        -> UserReadSchema:
    user = await get_user_by_name(username, session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.username != active_user.username and not active_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have permission to access this user")

    return UserReadSchema(id=user.id, username=user.username, email=user.email,
                          is_active=user.is_active)
