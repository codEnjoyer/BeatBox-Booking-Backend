from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.dependencies.booking import OwnedBookingDep
from src.api.dependencies.room import ValidRoomInStudioDep
from src.api.dependencies.services import BookingServiceDep
from src.api.dependencies.auth import AuthenticatedUser
from src.domain.models.booking import BookingStatus
from src.domain.schemas.booking import BookingCreate, BookingRead, BookingUpdate

router = APIRouter(tags=["Booking"])


@router.post(
    "/studios/{studio_id}/rooms/{room_name}/bookings",
    response_model=BookingRead,
)
async def book_slot(
    room: ValidRoomInStudioDep,
    schema: BookingCreate,
    service: BookingServiceDep,
    user: AuthenticatedUser,
) -> BookingRead:
    booking = await service.create(
        schema=schema, user_id=user.id, studio_id=room.studio_id
    )
    # TODO: улучшить
    if schema.status == BookingStatus.CLOSED and not user.employee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to close the booking",
        )
    return booking


@router.get("/me/bookings", response_model=list[BookingRead])
async def get_user_bookings(
    service: BookingServiceDep,
    user: AuthenticatedUser,
    offset: int = 0,
    limit: int = 100,
) -> list[BookingRead]:
    bookings = await service.get_user_bookings(
        user.id, offset=offset, limit=limit
    )
    return bookings


@router.put("/{booking_id}", response_model=BookingRead)
async def update_booking(
    booking: OwnedBookingDep,
    schema: BookingUpdate,
    service: BookingServiceDep,
    user: AuthenticatedUser,
) -> BookingRead:
    booking = await service.update_booking(
        booking.id, user_id=user.id, schema=schema
    )
    return booking


@router.delete("/me/bookings/{booking_id}")
async def cancel_booking(
    booking: OwnedBookingDep, service: BookingServiceDep, _: AuthenticatedUser
) -> None:
    await service.delete_by_id(booking.id)
