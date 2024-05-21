import uuid

from fastapi import APIRouter, Depends

from src.api.dependencies.services.booking import BookingServiceDep
from src.api.dependencies.auth import manager
from src.domain.schemas.booking import BookingCreate, BookingRead, BookingUpdate
from src.domain.models.user import User
from src.api.dependencies.booking import convert_model_to_scheme

router = APIRouter(prefix="/slots", tags=["Slot"])


@router.post("", response_model=BookingRead)
async def booked_slot(
    studio_id: int,
    schema: BookingCreate,
    service: BookingServiceDep,
    user: User = Depends(manager),
) -> BookingRead:
    review = await service.create(
        schema=schema, user_id=user.id, studio_id=studio_id
    )
    return convert_model_to_scheme(review)


@router.get("/my", response_model=list[BookingRead])
async def get_user_slots(
    service: BookingServiceDep,
    user: User = Depends(manager),
    offset: int = 0,
    limit: int = 100,
) -> list[BookingRead]:
    slots = await service.get_slots_by_user_id(
        user_id=user.id, offset=offset, limit=limit
    )
    return [convert_model_to_scheme(slot) for slot in slots]


@router.delete("/{slot_id}", response_model=str)
async def remove_slot(
    slot_id: uuid.UUID,
    service: BookingServiceDep,
    user: User = Depends(manager),
) -> str:
    await service.remove(slot_id=slot_id, user_id=user.id)
    return "Success delete"


@router.put("/{slot_id}", response_model=BookingRead)
async def patch_slot(
    slot_id: uuid.UUID,
    schema: BookingUpdate,
    service: BookingServiceDep,
    user: User = Depends(manager),
) -> BookingRead:
    slot = await service.patch_slot(
        slot_id=slot_id, user_id=user.id, schema=schema
    )
    return convert_model_to_scheme(slot)
