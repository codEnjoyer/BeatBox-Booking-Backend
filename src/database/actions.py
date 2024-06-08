from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.dependencies.phone_number import validate_number

from src.domain.models.user import User
from src.domain.schemas.user import UserCreateSchema
from src.domain.dependencies.auth import hash_password


async def create_user(
    user_schema: UserCreateSchema, session: AsyncSession
) -> User:
    formatted_number = validate_number(user_schema.phone_number)
    new_user = User(
        email=user_schema.email,
        hashed_password=hash_password(user_schema.password),
        is_superuser=user_schema.is_superuser,
        phone_number=formatted_number,
    )
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    await session.commit()
    return new_user
