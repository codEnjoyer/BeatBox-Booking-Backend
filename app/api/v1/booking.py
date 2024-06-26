from fastapi import APIRouter, HTTPException
from starlette import status

from api.v1.dependencies.auth import AuthenticatedUser
from api.v1.dependencies.booking import (
    OwnedBookingDep,
    BookingCancelerDep,
    ValidBookingIdDep,
)
from api.v1.dependencies.room import ValidStudioRoomIdDep
from api.v1.dependencies.services import BookingServiceDep
from api.v1.dependencies.types import (
    QueryLimit,
    QueryOffset,
    QueryDateFrom,
    QueryDateTo,
)
from exceptions.booking import (
    MustBookWithinOneDayException,
    MustBookWithinStudioWorkingTimeException,
    SlotAlreadyBookedException,
    BookingAlreadyCancelledException,
    BookingMustBeActiveException,
)
from schemas.booking import BookingCreate, BookingRead, BookingUpdate

router = APIRouter(tags=["Booking"])


@router.get("/users/me/bookings", response_model=list[BookingRead])
async def get_my_bookings(
    booking_service: BookingServiceDep,
    user: AuthenticatedUser,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[BookingRead]:
    bookings = await booking_service.get_user_bookings(
        user.id, offset=offset, limit=limit
    )
    return bookings


@router.get(
    "/studios/{studio_id}/rooms/{room_id}/bookings",
    response_model=list[BookingRead],
)
async def get_room_bookings(
    room: ValidStudioRoomIdDep,
    booking_service: BookingServiceDep,
    from_: QueryDateFrom | None = None,
    to: QueryDateTo | None = None,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
):
    room_bookings = await booking_service.get_room_bookings(
        room.id, from_, to, offset=offset, limit=limit
    )
    return room_bookings


@router.post(
    "/studios/{studio_id}/rooms/{room_id}/bookings",
    response_model=BookingRead,
)
async def book_room(
    room: ValidStudioRoomIdDep,
    schema: BookingCreate,
    booking_service: BookingServiceDep,
    user: AuthenticatedUser,
) -> BookingRead:
    try:
        booking = await booking_service.book_room_for_user(
            room, user.id, schema
        )
    except (
        MustBookWithinOneDayException,
        MustBookWithinStudioWorkingTimeException,
    ) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except SlotAlreadyBookedException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e)) from e
    return booking


@router.put(
    "/studios/{studio_id}/rooms/{room_id}/bookings/{booking_id}",
    response_model=BookingRead,
)
async def update_booking_name(
    booking: OwnedBookingDep,
    schema: BookingUpdate,
    booking_service: BookingServiceDep,
    _: AuthenticatedUser,
) -> BookingRead:
    try:
        booking = await booking_service.update_by_id(booking.id, schema)
    except BookingMustBeActiveException as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return booking


@router.delete(
    "/studios/{studio_id}/rooms/{room_id}/bookings/{booking_id}",
    response_model=BookingRead,
)
async def cancel_booking(
    booking: ValidBookingIdDep,
    _: BookingCancelerDep,
    booking_service: BookingServiceDep,
) -> None:
    try:
        cancelled = await booking_service.cancel_booking(booking)
    except BookingAlreadyCancelledException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e)) from e
    return cancelled
