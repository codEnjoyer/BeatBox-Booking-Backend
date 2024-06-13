import uuid
from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from src.api.dependencies.auth import AuthenticatedUser
from src.api.dependencies.services import BookingServiceDep
from src.domain.exceptions.booking import BookingNotFoundException
from src.domain.models import Booking


async def valid_booking_id(
    booking_id: uuid.UUID, booking_service: BookingServiceDep
) -> Booking:
    try:
        booking = await booking_service.get_by_id(booking_id)
    except BookingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return booking


ValidBookingIdDep = Annotated[Booking, Depends(valid_booking_id)]


async def owned_booking(
    booking: ValidBookingIdDep, user: AuthenticatedUser
) -> Booking:
    if booking.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be owner of this booking",
        )
    return booking


OwnedBookingDep = Annotated[Booking, Depends(owned_booking)]
