from abc import ABC

from sqlalchemy import ColumnElement, update

from src.domain.models.base import BaseModel
from src.domain.db import async_session_maker
from src.domain.schemas.base import BaseSchema
from src.infrastructure.item.operations.update import UpdateOperation


class ORMUpdate[Model: BaseModel, UpdateSchema: BaseSchema] \
            (UpdateOperation[Model, UpdateSchema],
             ABC):

    async def update(self,
                     schema: UpdateSchema | dict[str, ...],
                     *where: ColumnElement[bool]) \
            -> Model:
        schema = schema.model_dump() if isinstance(schema, BaseSchema) else schema
        async with async_session_maker() as session:
            stmt = (update(self._model)
                    .where(*where)
                    .values(**schema)
                    .returning(self._model))
            result = await session.execute(stmt)
            instances = result.scalars()
            await session.commit()
            return instances
