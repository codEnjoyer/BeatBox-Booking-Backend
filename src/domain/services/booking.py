import datetime
from typing import override

from src.domain.models import Room
from src.domain.models.booking import Booking, BookingStatus
from src.domain.schemas.booking import BookingCreate, BookingUpdate
from src.domain.exceptions.booking import (
    BookingNotFoundException,
    MustBookWithinOneDayException,
    SlotAlreadyBookedException,
    MustBookWithinStudioWorkingTimeException,
    BookingAlreadyCancelledException,
    BookingMustBeActiveException,
)
from src.domain.models.repositories.booking import BookingRepository
from src.domain.services.base import ModelService


class BookingService(
    ModelService[BookingRepository, Booking, BookingCreate, BookingUpdate]
):
    def __init__(self):
        super().__init__(BookingRepository(), BookingNotFoundException)

    async def get_room_bookings(
        self,
        room_id: int,
        from_: datetime.date | None = None,
        to: datetime.date | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Booking]:
        date_filter = []
        if from_:
            date_filter.append(self.model.starts_at >= from_)
        if to:
            date_filter.append(self.model.ends_at < to)
        return await self._repository.get_all(
            self.model.room_id == room_id,
            *date_filter,
            offset=offset,
            limit=limit,
        )

    async def book_room_for_user(
        self, room: Room, user_id: int, schema: BookingCreate
    ) -> Booking:
        await self.check_if_can_be_booked(room, schema)
        schema_dict = schema.model_dump()
        schema_dict.update(
            user_id=user_id,
            room_id=room.id,
            status=BookingStatus.BOOKED,
        )
        created = await self._repository.create(schema_dict)
        with_user = await self.get_by_id(created.id)
        return with_user

    @override
    async def update_by_id(
        self, booking_id: int, schema: BookingUpdate
    ) -> Booking:
        updated = await super().update_by_id(booking_id, schema)
        return await self.get_by_id(updated.id)

    async def update_booking_name(
        self, booking: Booking, schema: BookingUpdate
    ) -> Booking:
        if booking.status != BookingStatus.BOOKED:
            raise BookingMustBeActiveException()

        return await self.update_by_id(booking.id, schema)

    async def cancel_booking(self, booking: Booking) -> Booking:
        return await self.update_by_id(
            booking.id, {"status": BookingStatus.CANCELLED}
        )

    @staticmethod
    async def check_if_can_be_booked(room: Room, schema: BookingCreate) -> None:
        if schema.starts_at.date() != schema.ends_at.date():
            raise MustBookWithinOneDayException()

        starts_at_time = schema.starts_at.time().replace(
            tzinfo=schema.starts_at.tzinfo
        )
        ends_at_time = schema.ends_at.time().replace(
            tzinfo=schema.ends_at.tzinfo
        )
        if (
            starts_at_time < room.studio.opening_at
            or ends_at_time > room.studio.closing_at
        ):
            raise MustBookWithinStudioWorkingTimeException()

        if not room.is_free_at_interval(
            from_=schema.starts_at, to=schema.ends_at
        ):
            raise SlotAlreadyBookedException()

    @staticmethod
    async def check_if_can_be_cancelled(booking: Booking) -> None:
        if booking.status == BookingStatus.CANCELLED:
            raise BookingAlreadyCancelledException()

    async def get_user_bookings(
        self, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[Booking]:
        return await self._repository.get_all(
            self.model.user_id == user_id, offset=offset, limit=limit
        )
