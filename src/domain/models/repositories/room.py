from typing import override, Iterable

from sqlalchemy import ColumnElement
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from src.domain.models import Room
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.room import RoomCreate, RoomUpdate


class RoomRepository(SQLAlchemyRepository[Room, RoomCreate, RoomUpdate]):
    @override
    @property
    def model(self) -> type[Room]:
        return Room

    @override
    async def get_all(
            self,
            *where: ColumnElement[bool],
            options: Iterable[ExecutableOption] | None = None,
            offset: int = 0,
            limit: int = 100,
    ) -> list[Room]:
        """
        Load rooms with bookings
        """
        options = options or ()
        rooms = await super().get_all(
            *where,
            options=(*options, selectinload(self.model.bookings)),
            offset=offset,
            limit=limit,
        )
        return rooms

    @override
    async def get_one(
            self,
            *where: ColumnElement[bool],
            options: Iterable[ExecutableOption] | None = None,
    ) -> Room:
        """
        Load room with bookings
        """
        options = options or ()
        room = await super().get_one(
            *where, options=(*options, selectinload(self.model.bookings))
        )
        return room
