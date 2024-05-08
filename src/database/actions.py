from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import User
from src.domain.schemas.user import UserCreateSchema


# TODO: Test exception by existing user
async def create_user(user_schema: UserCreateSchema, session: AsyncSession) -> User:
    new_user = User(**user_schema.model_dump())
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    await session.commit()
    return new_user
