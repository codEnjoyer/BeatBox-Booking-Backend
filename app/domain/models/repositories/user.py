from typing import override

from app.domain.models import User
from app.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from app.domain.schemas.user import UserCreate, UserUpdate


class UserRepository(SQLAlchemyRepository[User, UserCreate, UserUpdate]):
    @override
    @property
    def model(self) -> type[User]:
        return User
