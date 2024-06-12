from src.domain.models import User
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.user import UserCreate, UserUpdate


class UserRepository(SQLAlchemyRepository[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)
