from typing import override

from src.domain.models import User
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.user import UserCreate, UserUpdate


class UserRepository(SQLAlchemyRepository[User, UserCreate, UserUpdate]):
    @override
    @property
    def model(self) -> type[User]:
        return User
