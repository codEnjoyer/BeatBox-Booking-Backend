from typing import Annotated

from fastapi import Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.db import async_session_maker
from src.domain.models import User
from src.settings import settings

manager = LoginManager(settings.secret_auth_token, token_url="/auth/token")

CurrentUser = Annotated[User, Depends(manager)]


class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int


async def get_user_by_name(username: str, session: AsyncSession) -> User | None:
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
