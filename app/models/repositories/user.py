from typing import override

from models import User
from models.repositories.SQLAlchemy import SQLAlchemyRepository
from schemas.user import UserCreate, UserUpdate


class UserRepository(SQLAlchemyRepository[User, UserCreate, UserUpdate]):
    @override
    @property
    def model(self) -> type[User]:
        return User
