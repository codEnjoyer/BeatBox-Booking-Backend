from typing import override

from sqlalchemy import ColumnElement, select, update
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.domain.db import async_session_maker
from src.domain.models import Studio
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.studio import StudioCreate, StudioUpdate


class StudioRepository(
    SQLAlchemyRepository[Studio, StudioCreate, StudioUpdate]
):
    @override
    @property
    def model(self) -> type[Studio]:
        return Studio

    async def is_studio_exist(self, *where: ColumnElement[bool]) -> bool:
        try:
            await self.get_one(*where)
        except NoResultFound:
            return False
        return True

    async def get(self, user_id: int, *where: ColumnElement[bool]) -> Studio:
        async with async_session_maker() as session:
            studio = await self.get_one_with_session(session, *where)

            employees = studio.employees
            if any(user_id == employee.user_id for employee in employees):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid permissions",
                )

            return studio

    async def get_one_with_session(
        self, session: AsyncSession, *where: ColumnElement[bool]
    ) -> Studio:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.employees))
            .where(*where)
            .limit(1)
        )
        result = await session.execute(stmt)
        studio: Studio | None = result.scalar()
        if not studio:
            raise NoResultFound
        return studio

    async def update_one(
        self, schema: StudioUpdate | dict[str, ...], *where: ColumnElement[bool]
    ) -> Studio:
        schema = (
            schema.model_dump() if isinstance(schema, StudioUpdate) else schema
        )
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(*where)
                .values(**schema)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            instances = result.scalar()
            await session.commit()
            return instances
