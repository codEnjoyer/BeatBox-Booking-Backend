from fastapi_login import LoginManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.db import async_session_maker
from src.domain.models import User
from src.settings import settings

manager = LoginManager(settings.secret_auth_token, token_url="/auth/token")


async def get_user_by_name(username: str, session: AsyncSession) -> User | None:
    stmt = select(User)
    stmt = stmt.filter_by(username=username)
    result = await session.execute(stmt)
    return result.unique().scalar_one()


@manager.user_loader()
async def get_user(name: str):
    async with async_session_maker() as db:
        return await get_user_by_name(name, db)
