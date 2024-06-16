from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.v1.dependencies.employee import StudioManagerDep
from src.api.v1.dependencies.services import FileServiceDep
from src.api.v1.dependencies.services import RoomServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep
from src.api.v1.dependencies.room import (
    convert_model_to_scheme,
    get_images_url,
    ValidStudioRoomNameDep,
)
from src.domain.exceptions.room import RoomWithSameNameAlreadyExistsException
from src.domain.models import Room
from src.domain.schemas.room import RoomRead, RoomCreate, RoomUpdate

router = APIRouter(tags=["Room"])


@router.get("/studios/{studio_id}/rooms", response_model=list[RoomRead])
async def get_all_studio_rooms(
    studio: ValidStudioIdDep, room_service: RoomServiceDep
) -> list[Room]:
    rooms = await room_service.get_all_in_studio(studio.id)
    return rooms


@router.get("/studios/{studio_id}/rooms/{room_name}", response_model=RoomRead)
async def get_studio_room(
    room: ValidStudioRoomNameDep,
) -> RoomRead:
    return room


@router.post("/studios/{studio_id}/rooms", response_model=RoomRead)
async def create_room(
    schema: RoomCreate,
    studio: ValidStudioIdDep,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    _: StudioManagerDep,
) -> RoomRead:
    try:
        room = await room_service.create_room_in_studio(studio.id, schema)
    except RoomWithSameNameAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )


@router.put("/studios/{studio_id}/rooms/{room_name}", response_model=RoomRead)
async def update_room(
    room: ValidStudioRoomNameDep,
    schema: RoomUpdate,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    _: StudioManagerDep,
) -> RoomRead:
    room = await room_service.update_by_id(room.id, schema)
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )


@router.delete(
    "/studios/{studio_id}/rooms/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room(
    room: ValidStudioRoomNameDep,
    room_service: RoomServiceDep,
    _: StudioManagerDep,
) -> None:
    await room_service.delete_by_id(room.id)
