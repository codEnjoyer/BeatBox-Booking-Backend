from src.domain.exceptions.user import (
    EmailAlreadyTakenException,
    NicknameAlreadyTakenException,
)
from src.domain.schemas.user import UserCreate
from src.domain.services.user import UserService
from src.settings import settings


async def load_users():
    user_service = UserService()
    root_user = UserCreate(
        email="root@mail.ru",
        nickname="root",
        password=settings.root_password,
    )
    try:
        await user_service.create(root_user, is_superuser=True)
    except (EmailAlreadyTakenException, NicknameAlreadyTakenException):
        pass


async def load_initial_data() -> None:
    await load_users()
