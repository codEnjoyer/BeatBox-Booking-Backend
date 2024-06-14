from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import User
from src.domain.models.repositories.user import UserRepository
from src.domain.schemas.user import UserCreate, UserUpdate
from src.domain.services.base import ModelService


class UserService(ModelService[UserRepository, User, UserCreate, UserUpdate]):
    pwd_context = CryptContext(schemes=["bcrypt"])

    def __init__(self):
        super().__init__(UserRepository(), UserNotFoundException)

    @staticmethod
    async def get_user_by_id(
        user_id: int, session: AsyncSession
    ) -> User | None:
        stmt = select(User)
        stmt = stmt.filter_by(id=user_id)
        result = await session.execute(stmt)
        return result.unique().scalar_one()

    @staticmethod
    async def get_user_by_email(
        email: str, session: AsyncSession
    ) -> User | None:
        stmt = select(User)
        stmt = stmt.filter_by(email=email)
        result = await session.execute(stmt)
        return result.unique().scalar_one()

    @staticmethod
    async def create_user(
        user_schema: UserCreate, session: AsyncSession
    ) -> User:
        new_user = User(
            email=user_schema.email,
            hashed_password=UserService.pwd_context.hash(user_schema.password),
            phone_number=user_schema.phone_number,
        )
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)
        await session.commit()
        return new_user

    @staticmethod
    def verify_password(plaintext: str, hashed: str):
        return UserService.pwd_context.verify(plaintext, hashed)
