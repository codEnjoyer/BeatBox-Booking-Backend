from fastapi import APIRouter
from starlette import status

from src.api.v1.dependencies.employee import StudioManagerDep

# from src.api.v1.dependencies.services import FileServiceDep
from src.api.v1.dependencies.services import RoomServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep
from src.api.v1.dependencies.room import (
    # convert_model_to_scheme,
    # get_images_url,
    ValidStudioRoomIdDep,
)
from src.domain.models import Room
from src.domain.schemas.room import RoomRead, RoomCreate, RoomUpdate

router = APIRouter(tags=["Room"])


@router.get("/studios/{studio_id}/rooms", response_model=list[RoomRead])
async def get_all_studio_rooms(
    studio: ValidStudioIdDep, room_service: RoomServiceDep
) -> list[Room]:
    rooms = await room_service.get_all_in_studio(studio.id)
    return rooms


@router.get("/studios/{studio_id}/rooms/{room_id}", response_model=RoomRead)
async def get_studio_room(
    room: ValidStudioRoomIdDep,
) -> RoomRead:
    return room


@router.post("/studios/{studio_id}/rooms", response_model=RoomRead)
async def create_room(
    studio: ValidStudioIdDep,
    schema: RoomCreate,
    room_service: RoomServiceDep,
    # file_service: FileServiceDep,
    _: StudioManagerDep,
) -> Room:
    room = await room_service.create_room_in_studio(studio.id, schema)
    return room
    # banner_url, images_url = await get_images_url(
    #     room=room, file_service=file_service, room_service=room_service
    # )
    # return convert_model_to_scheme(
    #     room=room, banner_url=banner_url, images_url=images_url
    # )


@router.put("/studios/{studio_id}/rooms/{room_id}", response_model=RoomRead)
async def update_room(
    room: ValidStudioRoomIdDep,
    schema: RoomUpdate,
    room_service: RoomServiceDep,
    # file_service: FileServiceDep,
    _: StudioManagerDep,
) -> RoomRead:
    # TODO: Check
    room = await room_service.update_by_id(room.id, schema)
    # banner_url, images_url = await get_images_url(
    #     room=room, file_service=file_service, room_service=room_service
    # )
    # return convert_model_to_scheme(
    #     room=room, banner_url=banner_url, images_url=images_url
    # )
    return room


@router.delete(
    "/studios/{studio_id}/rooms/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room(
    room: ValidStudioRoomIdDep,
    room_service: RoomServiceDep,
    _: StudioManagerDep,
) -> None:
    await room_service.delete_by_id(room.id)
