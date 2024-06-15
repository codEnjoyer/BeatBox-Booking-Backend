from typing import Tuple, Annotated

from fastapi import HTTPException, Depends
from starlette import status

from src.api.v1.dependencies.services import RoomServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep
from src.domain.exceptions.room import RoomNotFoundException
from src.domain.models.room import Room
from src.domain.schemas.room import RoomRead
from src.domain.services.file import FileService
from src.domain.services.room import RoomService
from sqlalchemy.exc import NoResultFound


def convert_model_to_scheme(
    room: Room,
    banner_url: str | None,
    images_url: list[str] | None,
) -> RoomRead:
    return RoomRead(
        name=room.name,
        description=room.description,
        banner=banner_url,
        images=images_url,
    )


async def get_images_url(
    room: Room, file_service: FileService, room_service: RoomService
) -> Tuple[str, list[str]]:
    banner_url = await file_service.try_get_url(name=room.banner_id)
    images_url = []

    try:
        images_id = await room_service.get_all_images(room_id=room.id)
    except NoResultFound:
        return banner_url, images_url

    images_url = [
        await file_service.get_url(name=image_id) for image_id in images_id
    ]
    return banner_url, images_url


async def valid_room_in_studio_by_name(
    room_name: str, studio: ValidStudioIdDep, room_service: RoomServiceDep
) -> Room:
    try:
        room = await room_service.get_by_name_in_studio(room_name, studio.id)
    except RoomNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return room


ValidStudioRoomNameDep = Annotated[Room, Depends(valid_room_in_studio_by_name)]
