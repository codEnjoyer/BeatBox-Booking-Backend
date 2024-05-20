from typing import override

from sqlalchemy import insert, ColumnElement, select, delete, update
from sqlalchemy.exc import NoResultFound

from src.domain.db import async_session_maker
from src.domain.models.base import BaseModel
from src.domain.schemas.base import BaseSchema
from src.infrastructure.repository import Repository


class SQLAlchemyRepository[
    Model: BaseModel, CreateSchema: BaseSchema, UpdateSchema: BaseSchema
](Repository[Model, CreateSchema, UpdateSchema]):

    @override
    @property
    def model(self) -> type[Model]:
        return self._model

    def __init__(self, model: type[Model]):
        super().__init__(model)

    async def create(self, schema: CreateSchema | dict[str, ...]) -> Model:
        schema = (
            schema.model_dump() if isinstance(schema, BaseSchema) else schema
        )
        async with async_session_maker() as session:
            stmt = insert(self._model).values(**schema).returning(self._model)
            result = await session.execute(stmt)
            instance = result.scalar()
            await session.commit()
            return instance

    async def get_all(
        self, *where: ColumnElement[bool], offset: int = 0, limit: int = 100
    ) -> list[Model]:
        async with async_session_maker() as session:
            stmt = select(self._model).where(*where).offset(offset).limit(limit)
            result = await session.execute(stmt)
            instances = result.scalars()
            return instances

    async def get_one(self, *where: ColumnElement[bool]) -> Model:
        async with async_session_maker() as session:
            stmt = select(self._model).where(*where).limit(1)
            result = await session.execute(stmt)
            instance: Model | None = result.scalar()
            if not instance:
                raise NoResultFound
            return instance

    async def update(
        self, schema: UpdateSchema | dict[str, ...], *where: ColumnElement[bool]
    ) -> Model:
        schema = (
            schema.model_dump() if isinstance(schema, BaseSchema) else schema
        )
        async with async_session_maker() as session:
            stmt = (
                update(self._model)
                .where(*where)
                .values(**schema)
                .returning(self._model)
            )
            result = await session.execute(stmt)
            instances = result.scalars().first()
            await session.commit()
            return instances

    async def delete(self, *where: ColumnElement[bool]) -> None:
        async with async_session_maker() as session: ## TODO: fix me pls
            stmt = delete(self._model).where(*where)
            await session.execute(stmt)
            await session.commit()
