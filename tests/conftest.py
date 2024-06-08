import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.main import app
from src.domain.db import Base, get_async_session
from src.settings import settings

engine_test = create_async_engine(str(settings.database_url), poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# По-хорошему добавить noqa, чтоб не подсвечивалось, но оставлю как есть
app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def test_env_file():
    # Проверка, что .env, используемый в тестах содержит ENVIRONMENT=TEST
    assert settings.environment == "TEST"


@pytest.fixture(scope="function")
async def clear_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="function")
async def prepare_database(test_env_file, clear_database):
    # Поскольку мы используем фикстуру clear_database заранее, то создавать тут таблички не надо
    yield  # Отдаём выполнение pytest

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Удаление всех таблиц в БД


# SETUP


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
