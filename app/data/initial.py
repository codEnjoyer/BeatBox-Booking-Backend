from app.domain.exceptions.user import (
    EmailAlreadyTakenException,
    NicknameAlreadyTakenException,
)
from app.domain.schemas.user import UserCreate
from app.domain.services.user import UserService
from app.settings import settings


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
