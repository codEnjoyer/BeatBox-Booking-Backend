from abc import ABC

from sqlalchemy import ColumnElement, delete

from src.db import async_session_maker
from src.domain.models.base import BaseModel
from src.infrastructure.item.operations.delete import DeleteOperation


class ORMDelete[Model: BaseModel](DeleteOperation[Model], ABC):

    async def delete(self,
                     *where: ColumnElement[bool]) \
            -> None:
        async with async_session_maker() as session:
            stmt = (delete(self._model)
                    .where(*where))
            await session.execute(stmt)
            await session.commit()
