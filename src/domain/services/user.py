from typing import override

from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound

from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import User
from src.domain.models.repositories.user import UserRepository
from src.domain.schemas.user import UserCreate, UserUpdate
from src.domain.services.base import ModelService


class UserService(ModelService[UserRepository, User, UserCreate, UserUpdate]):
    _pwd_context = CryptContext(schemes=["bcrypt"],
                                deprecated="auto")

    def __init__(self):
        super().__init__(UserRepository(), UserNotFoundException)

    async def get_by_email(self, email: str) -> User:
        try:
            model = await self._repository.get_one(self.model.email == email)
        except NoResultFound as e:
            raise self._not_found_exception from e
        return model

    @override
    async def create(self, schema: UserCreate) -> User:
        # TODO: добавить проверки
        schema_dict = schema.model_dump()
        plain_password = schema_dict.pop("password")
        schema_dict["hashed_password"] = self._hash_password(plain_password)
        return await self._repository.create(schema_dict)

    def is_password_valid(self, plain: str, hashed: str) -> bool:
        return self._pwd_context.verify(plain, hashed)

    def _hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)
