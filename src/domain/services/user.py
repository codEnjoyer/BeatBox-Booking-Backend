from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import User
from src.domain.models.repositories.user import UserRepository
from src.domain.schemas.user import UserCreateSchema, UserUpdateSchema
from src.domain.services.base import ModelService


class UserService(ModelService[
                      UserRepository, User, UserCreateSchema,
                      UserUpdateSchema]):
    def __init__(self):
        super().__init__(UserRepository(), UserNotFoundException)
