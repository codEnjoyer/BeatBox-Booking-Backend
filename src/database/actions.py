from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import async_session_maker
from src.models.user import User
from src.security import manager
from src.schemas.user import UserCreateSchema


async def get_user_by_name(username: str, session: AsyncSession) -> Optional[User]:
    stmt = select(User)
    stmt = stmt.filter_by(
        username=username
    )
    result = await session.execute(stmt)
    return result.unique().scalar_one()


@manager.user_loader()
async def get_user(name: str):
    async with async_session_maker() as db:
        return await get_user_by_name(name, db)


#TODO: Test exception by existing user
async def create_user(user_schema: UserCreateSchema, session: AsyncSession) -> User:
    new_user = User(**user_schema.model_dump())
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    await session.commit()
    return new_user
