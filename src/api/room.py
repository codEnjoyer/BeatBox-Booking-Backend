from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.dependencies.services import FileServiceDep
from src.api.dependencies.services import RoomServiceDep
from src.api.dependencies.studio import StudioEmployeeDep
from src.domain.exceptions.room import RoomWithSameNameAlreadyExistsException
from src.domain.schemas.room import RoomRead, RoomCreate, RoomUpdate
from src.api.dependencies.room import (
    convert_model_to_scheme,
    get_images_url,
    ValidRoomInStudioDep,
)

router = APIRouter(tags=["Room"])


@router.get("/studios/{studio_id}/rooms/{room_name}", response_model=RoomRead)
async def get_room(
    room: ValidRoomInStudioDep,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
) -> RoomRead:
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )


@router.post("/studios/{studio_id}/rooms", response_model=RoomRead)
async def create_room_in_studio(
    schema: RoomCreate,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    studio_employee: StudioEmployeeDep,
) -> RoomRead:
    try:
        room = await room_service.create_room_in_studio(
            studio_employee.studio_id, schema
        )
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
    room: ValidRoomInStudioDep,
    schema: RoomUpdate,
    room_service: RoomServiceDep,
    file_service: FileServiceDep,
    _: StudioEmployeeDep,
) -> RoomRead:
    room = await room_service.update_by_id(schema, room.id)
    banner_url, images_url = await get_images_url(
        room=room, file_service=file_service, room_service=room_service
    )
    return convert_model_to_scheme(
        room=room, banner_url=banner_url, images_url=images_url
    )


@router.delete("/studios/{studio_id}/rooms/{room_id}")
async def delete_room(
    room: ValidRoomInStudioDep,
    room_service: RoomServiceDep,
    _: StudioEmployeeDep,
) -> None:
    await room_service.delete_by_id(room.id)
