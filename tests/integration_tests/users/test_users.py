import pytest
from app.domain.models import User
from sqlalchemy import select

from tests.conftest import async_session_maker


@pytest.mark.usefixtures("clear_database", "create_users")
class TestUsers:
    async def test_count_users(self):
        async with async_session_maker() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            users = result.scalars().all()

            assert len(users) == 3
