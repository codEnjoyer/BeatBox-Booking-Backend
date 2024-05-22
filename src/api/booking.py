import uuid

from fastapi import APIRouter

from src.api.dependencies.services.booking import BookingServiceDep
from src.api.dependencies.auth import AuthenticatedUser
from src.domain.schemas.booking import BookingCreate, BookingRead, BookingUpdate
from src.api.dependencies.booking import convert_model_to_scheme

router = APIRouter(prefix="/bookings", tags=["Booking"])


@router.post("", response_model=BookingRead)
async def booked_slot(
    studio_id: int,
    schema: BookingCreate,
    service: BookingServiceDep,
    user: AuthenticatedUser,
) -> BookingRead:
    review = await service.create(
        schema=schema, user_id=user.id, studio_id=studio_id
    )
    return convert_model_to_scheme(review)


@router.get("/my", response_model=list[BookingRead])
async def get_user_bookings(
    service: BookingServiceDep,
    user: AuthenticatedUser,
    offset: int = 0,
    limit: int = 100,
) -> list[BookingRead]:
    bookings = await service.get_bookings_by_user_id(
        user_id=user.id, offset=offset, limit=limit
    )
    return [convert_model_to_scheme(booking) for booking in bookings]


@router.delete("/{booking_id}", response_model=str)
async def remove_booking(
    booking_id: uuid.UUID, service: BookingServiceDep, user: AuthenticatedUser
) -> str:
    await service.remove(booking_id=booking_id, user_id=user.id)
    return "Success delete"


@router.put("/{booking_id}", response_model=BookingRead)
async def patch_booking(
    booking_id: uuid.UUID,
    schema: BookingUpdate,
    service: BookingServiceDep,
    user: AuthenticatedUser,
) -> BookingRead:
    booking = await service.patch_booking(
        booking_id=booking_id, user_id=user.id, schema=schema
    )
    return convert_model_to_scheme(booking)