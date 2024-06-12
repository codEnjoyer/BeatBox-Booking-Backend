from abc import abstractmethod

from sqlalchemy import insert, ColumnElement, select, delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.base import ExecutableOption

from src.domain.db import async_session_maker
from src.domain.models.base import BaseModel
from src.domain.schemas.base import BaseSchema
from src.infrastructure.repository import Repository


class SQLAlchemyRepository[
    Model: BaseModel, CreateSchema: BaseSchema, UpdateSchema: BaseSchema
](Repository[Model, CreateSchema, UpdateSchema]):

    @abstractmethod
    @property
    def model(self) -> type[Model]: ...

    async def create(self, schema: CreateSchema | dict[str, ...]) -> Model:
        schema = (
            schema.model_dump() if isinstance(schema, BaseSchema) else schema
        )
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**schema).returning(self.model)
            result = await session.execute(stmt)
            instance = result.scalar()
            await session.commit()
            return instance

    async def get_all(
        self,
        *where: ColumnElement[bool],
        options: tuple[ExecutableOption] | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Model]:
        """
        Raises:
            NoResultFound
        """
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .where(*where)
                .options(*options)
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(stmt)
            instances = result.unique().scalars().all()
            if not instances:
                raise NoResultFound
            return instances

    async def get_one(
        self,
        *where: ColumnElement[bool],
        options: tuple[ExecutableOption] | None = None,
    ) -> Model:
        """
        Raises:
            NoResultFound
        """
        async with async_session_maker() as session:
            stmt = select(self.model).where(*where).options(*options).limit(1)
            result = await session.execute(stmt)
            instance: Model | None = result.scalar()
            if not instance:
                raise NoResultFound
            return instance

    async def update(
        self, schema: UpdateSchema | dict[str, ...], *where: ColumnElement[bool]
    ) -> Model | list[Model]:
        schema = (
            schema.model_dump() if isinstance(schema, BaseSchema) else schema
        )
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(*where)
                .values(**schema)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            instances = result.scalars()
            await session.commit()
            return instances[0] if len(instances) == 1 else instances

    async def delete(self, *where: ColumnElement[bool]) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(*where)
            await session.execute(stmt)
            await session.commit()
