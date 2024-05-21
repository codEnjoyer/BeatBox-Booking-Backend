from fastapi_login import LoginManager
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import User
from src.settings import settings

manager = LoginManager(settings.secret_auth_token, token_url="/auth/token")


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    try:
        stmt = select(User)
        stmt = stmt.filter_by(email=email)
        result = await session.execute(stmt)
        return result.unique().scalar_one()
    except NoResultFound:
        raise UserNotFoundException()


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    try:
        stmt = select(User)
        stmt = stmt.filter_by(id=user_id)
        result = await session.execute(stmt)
        return result.unique().scalar_one()
    except NoResultFound:
        raise UserNotFoundException()

