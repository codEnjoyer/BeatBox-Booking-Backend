import datetime
from fastapi import APIRouter

from src.api.dependencies.booking import (
    OwnedBookingDep,
    BookingCancelerDep,
    ValidBookingIdDep,
)
from src.api.dependencies.room import ValidStudioRoomNameDep
from src.api.dependencies.services import BookingServiceDep
from src.api.dependencies.auth import AuthenticatedUser
from src.api.dependencies.studio import ValidStudioIdDep
from src.api.dependencies.types import QueryLimit, QueryOffset
from src.domain.schemas.booking import BookingCreate, BookingRead, BookingUpdate

router = APIRouter(tags=["Booking"])


@router.get("/me/bookings", response_model=list[BookingRead])
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


@router.get("/studios/{studio_id}/bookings", response_model=list[BookingRead])
async def get_studio_bookings(
    studio: ValidStudioIdDep,
    booking_service: BookingServiceDep,
    _: AuthenticatedUser,
    from_: datetime.date | None = None,
    to: datetime.date | None = None,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
):
    studio_bookings = []
    for room in studio.rooms:
        room_bookings = await booking_service.get_room_bookings(
            room.id, from_, to, offset=offset, limit=limit
        )
        studio_bookings.extend(room_bookings)
    return studio_bookings


@router.get(
    "/studios/{studio_id}/rooms/{room_name}/bookings",
    response_model=list[BookingRead],
)
async def get_room_bookings(
    room: ValidStudioRoomNameDep,
    _: AuthenticatedUser,
    booking_service: BookingServiceDep,
    from_: datetime.date | None = None,
    to: datetime.date | None = None,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
):
    room_bookings = await booking_service.get_room_bookings(
        room.id, from_, to, offset=offset, limit=limit
    )
    return room_bookings


@router.post(
    "/studios/{studio_id}/rooms/{room_name}/bookings",
    response_model=BookingRead,
)
async def book_slot(
    schema: BookingCreate,
    room: ValidStudioRoomNameDep,
    booking_service: BookingServiceDep,
    user: AuthenticatedUser,
) -> BookingRead:
    booking = await booking_service.book_room_for_user(room, user.id, schema)
    # booking = await booking_service.create(
    #     schema=schema, user_id=user.id, studio_id=room.studio_id
    # )
    # # TODO: улучшить
    # if schema.status == BookingStatus.CLOSED and not user.employee:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="User does not have permission to close the booking",
    #     )
    return booking


@router.put(
    "/studios/{studio_id}/rooms/{room_name}/bookings/{booking_id}",
    response_model=BookingRead,
)
async def confirm_payment_for_booking(
    schema: BookingUpdate,
    booking: OwnedBookingDep,
    booking_service: BookingServiceDep,
    user: AuthenticatedUser,
) -> BookingRead:
    # TODO: заменить на соответствующую логику
    booking = await booking_service.update_booking(
        booking.id, user_id=user.id, schema=schema
    )
    return booking


@router.delete("/studios/{studio_id}/rooms/{room_name}/bookings/{booking_id}")
async def cancel_booking(
    booking: ValidBookingIdDep,
    _: BookingCancelerDep,
    booking_service: BookingServiceDep,
) -> None:
    await booking_service.delete_by_id(booking.id)
