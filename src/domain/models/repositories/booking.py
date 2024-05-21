from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import selectinload

from src.domain.db import async_session_maker
from src.domain.models import Booking
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.booking import BookingCreate, BookingUpdate
from src.domain.exceptions.booking import BookingNotFoundException


class BookingRepository(
    SQLAlchemyRepository[Booking, BookingCreate, BookingUpdate]
):
    def __init__(self):
        super().__init__(Booking)

    async def get_one_with_room_relation(
        self, *where: ColumnElement[bool]
    ) -> Booking:
        async with async_session_maker() as session:
            stmt = (
                select(self._model)
                .options(selectinload(self._model.room))
                .where(*where)
                .limit(1)
            )
            result = await session.execute(stmt)
            room: Booking | None = result.scalar()
            if not room:
                raise BookingNotFoundException
            return room
