from src.domain.models import User
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.user import UserCreateSchema, UserUpdateSchema


class UserRepository(
    SQLAlchemyRepository[User, UserCreateSchema, UserUpdateSchema]
):
    def __init__(self):
        super().__init__(User)
