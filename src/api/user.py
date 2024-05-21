from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.services.auth import get_user_by_id, manager, get_user_by_email
from src.domain.db import get_async_session, async_session_maker
from src.domain.schemas.user import UserReadSchema
from src.domain.models.user import User

router = APIRouter(prefix="/users", tags=["User"])


@manager.user_loader()
async def get_user(email: str):
    async with async_session_maker() as db:
        return await get_user_by_email(email, db)


@router.get("/", response_model=list[UserReadSchema])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}")
async def read_user(
        user_id: int,
        active_user: User = Depends(manager),
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
