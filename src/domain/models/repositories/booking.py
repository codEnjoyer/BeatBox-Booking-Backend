from typing import override

from sqlalchemy import ColumnElement, select, update
from sqlalchemy.orm import selectinload

from src.domain.db import async_session_maker
from src.domain.models import Booking
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.booking import BookingCreate, BookingUpdate
from src.domain.exceptions.booking import BookingNotFoundException


class BookingRepository(
    SQLAlchemyRepository[Booking, BookingCreate, BookingUpdate]
):
    @override
    @property
    def model(self) -> type[Booking]:
        return Booking

    async def get_one_with_room_relation(
        self, *where: ColumnElement[bool]
    ) -> Booking:
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .options(selectinload(self.model.room))
                .where(*where)
                .limit(1)
            )
            result = await session.execute(stmt)
            booking: Booking | None = result.scalar()
            if not booking:
                raise BookingNotFoundException
            return booking

    async def update_one(
        self,
        schema: BookingUpdate | dict[str, ...],
        *where: ColumnElement[bool],
    ) -> Booking:
        schema = (
            schema.model_dump() if isinstance(schema, BookingUpdate) else schema
        )
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(*where)
                .values(**schema)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            instance = result.scalar()
            await session.commit()
            return instance
