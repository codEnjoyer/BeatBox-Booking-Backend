from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.database.actions import create_user, get_user_by_name
from src.schemas.user import UserCreateSchema, UserReadSchema
from src.security import manager
from src.models.user import User

router = APIRouter(prefix="/user")


@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def register(user_schema: UserCreateSchema, session: AsyncSession = Depends(get_async_session)) -> UserReadSchema:
    try:
        user = await create_user(user_schema=user_schema, session=session)
        return UserReadSchema(id = user.id, username=user.username, email=user.email, is_active=user.is_active, is_superuser=user.is_superuser)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

#services
@router.get("/", response_model=list[UserReadSchema])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{username}")
async def read_user(
    username, active_user=Depends(manager), session: AsyncSession = Depends(get_async_session)
) -> UserReadSchema:
    user = await get_user_by_name(username, session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.username != active_user.username and not active_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this user") 

    return UserReadSchema(id = user.id, username=user.username, email=user.email, is_active=user.is_active)
