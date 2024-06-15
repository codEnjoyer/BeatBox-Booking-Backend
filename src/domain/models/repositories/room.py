import uuid
from typing import override

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.domain.db import async_session_maker
from src.domain.models import Room, Studio
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.room import RoomCreate, RoomUpdate


class RoomRepository(SQLAlchemyRepository[Room, RoomCreate, RoomUpdate]):
    @override
    @property
    def model(self) -> type[Room]:
        return Room

    @staticmethod
    async def is_working_in_studio(employee_id: int, studio_id: int) -> bool:
        # TODO: перенести в зависимости
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
            studio_employees_ids = (
                employee.id for employee in studio.employees
            )
            return employee_id in studio_employees_ids

    @staticmethod
    async def get_all_images_by_id(room_id: int) -> list[uuid.UUID]:
        # async with async_session_maker() as session:
        #     stmt = select(RoomImage).where(RoomImage.room_id == room_id)
        #     result = await session.execute(stmt)
        #     instances = result.unique().scalars().all()
        #     if not instances:
        #         raise NoResultFound
        #     return instances
        raise NotImplementedError
