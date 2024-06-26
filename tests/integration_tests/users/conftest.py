import pytest
from app.domain.models import User
from sqlalchemy import delete

from app.domain.schemas.user import UserCreate
from tests.conftest import async_session_maker


@pytest.fixture
def users_create_schema():
    users = [
        UserCreate(username="test_1", email="test1@testmail.com", hashed_password="my_secret_password"),
        UserCreate(username="test-2", email="test2@testmail.com", hashed_password="my_secret_password2"),
        UserCreate(username="test=3", email="test3@testmail.com", hashed_password="my_secret_password3"),
    ]
    return users


@pytest.fixture(scope="function")
async def empty_users():
    async with async_session_maker() as session:
        stmt = delete(User)

        await session.execute(stmt)
        await session.commit()


@pytest.fixture(scope="function")
async def create_users(users_create_schema):
    async with async_session_maker() as session:

        # Добавление пользователей в БД
        for user_create_schema in users_create_schema:
            new_user = User(**user_create_schema.model_dump())

            session.add(new_user)
            await session.flush()
            await session.refresh(new_user)
            await session.commit()

        # await session.close()
