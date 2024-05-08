from abc import ABC

from sqlalchemy import insert

from src.domain.models.base import BaseModel
from src.domain.db import async_session_maker
from src.domain.schemas.base import BaseSchema
from src.infrastructure.item.operations.create import CreateOperation


class ORMCreate[Model: BaseModel, CreateSchema: BaseSchema] \
            (CreateOperation[Model, CreateSchema],
             ABC):

    async def create(self,
                     schema: CreateSchema | dict[str, ...]) \
            -> Model:
        schema = schema.model_dump() if isinstance(schema, BaseSchema) else schema
        async with async_session_maker() as session:
            stmt = (insert(self._model)
                    .values(**schema)
                    .returning(self._model))
            result = await session.execute(stmt)
            instance = result.scalar()
            await session.commit()
            return instance
