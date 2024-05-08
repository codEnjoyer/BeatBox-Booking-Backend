from abc import ABC

from sqlalchemy import ColumnElement, select
from sqlalchemy.exc import NoResultFound

from src.domain.models.base import BaseModel
from src.domain.db import async_session_maker
from src.infrastructure.item.operations.read import GetOneOperation, GetAllOperation


class ORMReadOne[Model: BaseModel](GetOneOperation[Model], ABC):

    async def get_one(self,
                      *where: ColumnElement[bool]) \
            -> Model:
        async with async_session_maker() as session:
            stmt = (select(self._model)
                    .where(*where)
                    .limit(1))
            result = await session.execute(stmt)
            instance: Model | None = result.scalar()
            if not instance:
                raise NoResultFound
            return instance


class ORMReadAll[Model: BaseModel](GetAllOperation[Model], ABC):
    async def get_all(self,
                      *where: ColumnElement[bool],
                      offset: int = 0,
                      limit: int = 100) \
            -> list[Model]:
        async with async_session_maker() as session:
            stmt = (select(self._model)
                    .where(*where)
                    .offset(offset)
                    .limit(limit))
            result = await session.execute(stmt)
            instances = result.scalars()
            return instances
