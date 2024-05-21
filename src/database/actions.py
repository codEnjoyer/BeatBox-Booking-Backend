from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.exceptions.user import UserAlreadyExistsException
from src.domain.models.user import User
from src.domain.schemas.user import UserCreateSchema
from src.domain.dependencies.auth import hash_password


async def create_user(
    user_schema: UserCreateSchema, session: AsyncSession
) -> User:
    try:
        new_user = User(
            email=user_schema.email,
            hashed_password=hash_password(user_schema.password),
            phone_number=user_schema.phone_number,
        )
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)
        await session.commit()
        return new_user
    except IntegrityError:
        raise UserAlreadyExistsException()
