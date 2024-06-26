from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base

from settings.db import db_settings

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_async_engine(
    db_settings.url,
    pool_recycle=60 * 60,  # 1 hour
    pool_size=10,
    max_overflow=20,
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
