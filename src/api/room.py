from fastapi import APIRouter, Depends, HTTPException
import datetime as dt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.api.dependencies.services.room import RoomServiceDep
from src.api.dependencies.services.studio import StudioServiceDep
from src.domain.models import Room
from src.domain.schemas.room import RoomRead, RoomCreate, RoomUpdate
from src.domain.schemas.booking import BookingRead
from src.api.dependencies.auth import manager
from src.domain.models.user import User
from src.api.dependencies.services.file import FileServiceDep
from src.api.dependencies.room import convert_model_to_scheme, get_images_url

router = APIRouter(prefix="/rooms", tags=["Room"])


@router.get("/{room_id}", response_model=RoomRead)
async def get_room(
    room_id: int, room_service: RoomServiceDep, file_service: FileServiceDep
) -> RoomRead:
    try:
        room = await room_service.get(room_id=room_id)
        banner_url, images_url = await get_images_url(
            room=room, file_service=file_service, room_service=room_service
        )
        return convert_model_to_scheme(
            room=room, banner_url=banner_url, images_url=images_url
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )


@router.get("/{room_id}/slots", response_model=list[BookingRead])
async def get_slots_in_studio(
    studio_id: int,
    start: dt.datetime,
    end: dt.datetime,
    studio_service: StudioServiceDep,
) -> list[BookingRead]:
    slots = await studio_service.get_slots(
        studio_id=studio_id, start=start, end=end
    )
    return slots


@router.get("/all/{studio_id}", response_model=list[RoomRead])
async def get_all_room_by_studio_id(
    studio_id: int,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
) -> list[RoomRead]:
    try:
        rooms = await room_service.get_all(Room.studio_id == studio_id)
        banner_and_images = [
            await get_images_url(
                room=room, file_service=file_service, room_service=room_service
            )
            for room in rooms
        ]

        return [
            convert_model_to_scheme(
                room=rooms[i],
                banner_url=banner_and_images[i][0],
                images_url=banner_and_images[i][1],
            )
            for i in range(len(rooms))
        ]

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )


@router.post("/{studio_id}", response_model=RoomRead)
async def create_room(
    studio_id: int,
    schema: RoomCreate,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    user: User = Depends(manager),
) -> RoomRead:
    room = await room_service.create(
        schema=schema, studio_id=studio_id, user_id=user.id
    )
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )


@router.delete("/{studio_id}/{room_id}", response_model=str)
async def delete_room(
    studio_id: int,
    room_id: int,
    room_service: RoomServiceDep,
    user: User = Depends(manager),
) -> str:
    await room_service.delete(
        room_id=room_id, studio_id=studio_id, user_id=user.id
    )
    return "Success delete"


@router.put("/{studio_id}/{room_id}", response_model=RoomRead)
async def update_room(
    studio_id: int,
    room_id: int,
    schema: RoomUpdate,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    user: User = Depends(manager),
) -> RoomRead:
    room = await room_service.update(
        room_id=room_id, studio_id=studio_id, user_id=user.id, schema=schema
    )
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )
