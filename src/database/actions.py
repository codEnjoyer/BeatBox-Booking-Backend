from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import User
from src.domain.schemas.user import UserCreateSchema
from src.domain.dependencies.auth import hash_password


# TODO: Test exception by existing user
async def create_user(
    user_schema: UserCreateSchema, session: AsyncSession
) -> User:
    new_user = User(
        username=user_schema.username,
        email=user_schema.email,
        hashed_password=hash_password(user_schema.password),
        is_superuser=user_schema.is_superuser,
    )
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    await session.commit()
    return new_user
