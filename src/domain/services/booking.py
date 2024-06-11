import datetime as dt
import uuid

from fastapi import HTTPException
from starlette import status
from sqlalchemy.exc import NoResultFound

from src.domain.models.booking import Booking, BookingStatus
from src.domain.schemas.booking import BookingCreate, BookingUpdate
from src.domain.exceptions.booking import BookingNotFoundException
from src.domain.models.repositories.booking import BookingRepository
from src.domain.models.repositories.room import RoomRepository
from src.domain.services.base import ModelService


class BookingService(
    ModelService[BookingRepository, Booking, BookingCreate, BookingUpdate]
):
    def __init__(self):
        super().__init__(BookingRepository(), BookingNotFoundException)

    async def create(self, schema: BookingCreate, **kwargs) -> Booking:
        user_id: int = kwargs.get('user_id')
        studio_id: int = kwargs.get('user_id')
        if await self.is_booking_already_booked(
                starts_at=schema.starts_at,
                ends_at=schema.ends_at,
                room_id=schema.room_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Booking already booked",
            )

        if (
                schema.status == BookingStatus.CLOSED
                and not await RoomRepository.check_employee_permissions(
            user_id=user_id, studio_id=studio_id
        )
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,  # TODO: replace to api layer exception
                detail="User does not have permission to close the booking",
            )
        booking_data = schema.dict()
        booking_data["user_id"] = user_id
        return await self._repository.create(booking_data)

    async def is_booking_already_booked(
            self, starts_at: dt.datetime, ends_at: dt.datetime, room_id: int
    ) -> bool:
        try:
            await self._repository.get_one(
                self._model.starts_at == starts_at,
                self._model.ends_at == ends_at,
                self._model.room_id == room_id,
                self._model.status == BookingStatus.BOOKED,
            )
        except NoResultFound:
            return False
        return True

    async def check_user_permission(
            self, booking_id: uuid.UUID, user_id: int
    ) -> bool:
        try:
            await self._repository.get_one(
                self._model.id == booking_id,
                self._model.user_id == user_id,
            )
        except NoResultFound:
            return False
        return True

    async def get_bookings_by_user_id(
            self, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[Booking]:
        return await self._repository.get_all(
            self._model.user_id == user_id, offset=offset, limit=limit
        )

    async def patch_booking(
            self, booking_id: uuid.UUID, user_id: int, schema: BookingUpdate
    ) -> Booking:
        if (
                schema.status == BookingStatus.CANCELED
                and not await self.check_user_permission(
            booking_id=booking_id, user_id=user_id
        )
        ):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="User does not have permission to cancel the booking",
            )

        booking = await self._repository.get_one_with_room_relation(
            self._model.id == booking_id
        )

        if (
                schema.status == BookingStatus.CLOSED
                and not await RoomRepository.check_employee_permissions(
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

        return await self._repository.update_one(
            booking_data, self._model.id == booking_id
        )

    async def remove(self, booking_id: uuid.UUID, user_id: int) -> None:
        if not await self.check_user_permission(
                booking_id=booking_id, user_id=user_id
        ):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="User does not have permission to delete the booking",
            )
        await self._repository.delete(self._model.id == booking_id)
