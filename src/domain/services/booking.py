import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status

from src.domain.models import Room
from src.domain.models.booking import Booking, BookingStatus
from src.domain.schemas.booking import BookingCreate, BookingUpdate
from src.domain.exceptions.booking import (
    BookingNotFoundException,
    MustBookWithinOneDayException,
    SlotAlreadyBookedException,
    MustBookWithinStudioWorkingTimeException,
)
from src.domain.models.repositories.booking import BookingRepository
from src.domain.models.repositories.room import RoomRepository
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
        limit: int = 100,
        offset: int = 0,
    ) -> list[Booking]:
        date_filter = []
        if from_:
            date_filter.append(self.model.starts_at >= from_)
        if to:
            date_filter.append(self.model.ends_at <= to)
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
            status=BookingStatus.WAITING_FOR_PAYMENT,
        )
        return await self._repository.create(schema_dict)

    @staticmethod
    async def check_if_can_be_booked(room: Room, schema: BookingCreate) -> None:
        if schema.starts_at.date() != schema.ends_at.date():
            raise MustBookWithinOneDayException()

        if (
            schema.starts_at < room.studio.opening_at
            or schema.ends_at > room.studio.closing_at
        ):
            raise MustBookWithinStudioWorkingTimeException()

        if not room.is_free_at_interval(
            from_=schema.starts_at, to=schema.ends_at
        ):
            raise SlotAlreadyBookedException()

    async def get_user_bookings(
        self, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[Booking]:
        return await self._repository.get_all(
            self.model.user_id == user_id, offset=offset, limit=limit
        )

    async def update_booking(
        self, booking_id: uuid.UUID, user_id: int, schema: BookingUpdate
    ) -> Booking:
        has_permission = await self.check_user_permission(booking_id, user_id)
        if schema.status == BookingStatus.CANCELED and not has_permission:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="User does not have permission to cancel the booking",
            )
        booking = await self._repository.get_one(
            self.model.id == booking_id, options=(selectinload(self.model.room))
        )

        if (
            schema.status == BookingStatus.CLOSED
            and not await RoomRepository.is_working_in_studio(
                user_id=user_id, studio_id=booking.room.studio_id
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have permission to close the booking",
            )

        booking_data = {
            "status": schema.status,
            "name": schema.name,
            "surname": schema.surname,
            "starts_at": schema.starts_at,
            "ends_at": schema.ends_at,
            "room_id": schema.room_id,
            "user_id": user_id,
        }

        result: Booking = await self._repository.update(
            booking_data, self.model.id == booking_id
        )
        return result
