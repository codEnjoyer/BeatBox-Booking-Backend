from exceptions.user import (
    EmailAlreadyTakenException,
    NicknameAlreadyTakenException,
)
from schemas.user import UserCreate
from services.user import UserService
from settings import app_settings


async def load_users():
    user_service = UserService()
    root_user = UserCreate(
        email="root@mail.ru",
        nickname="root",
        password=app_settings.root_password,
    )
    try:
        await user_service.create(root_user, is_superuser=True)
    except (EmailAlreadyTakenException, NicknameAlreadyTakenException):
        pass


async def load_initial_data() -> None:
    await load_users()
