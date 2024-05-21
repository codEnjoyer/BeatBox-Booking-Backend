import uuid

from sqlalchemy import ColumnElement, select, update
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.domain.db import async_session_maker
from src.domain.models import Room, Studio, RoomImage
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.room import RoomCreate, RoomUpdate


class RoomRepository(SQLAlchemyRepository[Room, RoomCreate, RoomUpdate]):
    def __init__(self):
        super().__init__(Room)

    @staticmethod
    async def check_employee_permissions(user_id: int, studio_id: int) -> None:
        async with async_session_maker() as session:
            stmt = (
                select(Studio)
                .where(Studio.id == studio_id)
                .options(selectinload(Studio.employees))
            )
            result = await session.execute(stmt)
            studio = result.scalar()
            if not studio:
                raise NoResultFound
            employees = studio.employees
            if not any(user_id == employee.user_id for employee in employees):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid permissions",
                )

    async def is_room_exist(self, *where: ColumnElement[bool]) -> bool:
        try:
            await self.get_one(*where)
        except NoResultFound:
            return False
        return True

    async def get(self, *where: ColumnElement[bool]) -> Room:
        async with async_session_maker() as session:
            return await self.get_one_with_session(session, *where)

    async def get_one_with_session(
        self, session: AsyncSession, *where: ColumnElement[bool]
    ) -> Room:
        stmt = (
            select(self._model)
            .options(
                selectinload(self._model.studio, self._model.studio.employees)
            )
            .where(*where)
            .limit(1)
        )
        result = await session.execute(stmt)
        room: Room | None = result.scalar()
        if not room:
            raise NoResultFound
        return room

    async def update_one(
        self, schema: RoomUpdate | dict[str, ...], *where: ColumnElement[bool]
    ) -> Room:
        schema = (
            schema.model_dump() if isinstance(schema, RoomUpdate) else schema
        )
        async with async_session_maker() as session:
            stmt = (
                update(self._model)
                .where(*where)
                .values(**schema)
                .returning(self._model)
            )
            result = await session.execute(stmt)
            instances = result.scalar()
            await session.commit()
            return instances

    @staticmethod
    async def get_all_images_by_id(room_id: int) -> list[uuid.UUID]:
        async with async_session_maker() as session:
            stmt = select(RoomImage).where(RoomImage.room_id == room_id)
            result = await session.execute(stmt)
            instances = result.unique().scalars().all()
            if not instances:
                raise NoResultFound
            return instances
