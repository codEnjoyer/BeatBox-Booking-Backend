from typing import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from asgi_lifespan import LifespanManager

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


# SETUP
@pytest.fixture(scope="session")
def sync_client() -> TestClient:
    with TestClient(app) as sync_client:
        yield sync_client


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        # Уберут подсветку ожидаемого типа app=app в след. версии либы httpx
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
            yield async_client
