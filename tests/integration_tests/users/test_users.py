import pytest
from sqlalchemy import select

from app.models import User
from tests.conftest import async_session_maker


@pytest.mark.usefixtures("clear_database", "create_users")
class TestUsers:
    async def test_count_users(self):
        async with async_session_maker() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            users = result.scalars().all()

            assert len(users) == 3
