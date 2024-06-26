import uuid
from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from api.v1.dependencies.auth import AuthenticatedUser
from api.v1.dependencies.room import ValidStudioRoomIdDep
from api.v1.dependencies.services import BookingServiceDep
from exceptions.booking import BookingNotFoundException
from models import Booking, User


async def valid_booking_id(
    booking_id: uuid.UUID,
    _: ValidStudioRoomIdDep,
    booking_service: BookingServiceDep,
) -> Booking:
    try:
        booking = await booking_service.get_by_id(booking_id)
    except BookingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    return booking


ValidBookingIdDep = Annotated[Booking, Depends(valid_booking_id)]


async def owned_booking(
    booking: ValidBookingIdDep, user: AuthenticatedUser
) -> Booking:
    if not booking.is_owned_by(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be owner of this booking",
        )
    return booking


OwnedBookingDep = Annotated[Booking, Depends(owned_booking)]


async def booking_canceler(
    booking: ValidBookingIdDep, user: AuthenticatedUser
) -> User:
    if not (
        booking.is_owned_by(user.id)
        or user.can_manage_studio(booking.room.studio.id)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    return user


BookingCancelerDep = Annotated[User, Depends(booking_canceler)]
