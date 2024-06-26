from typing import Tuple, Annotated

from fastapi import HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from starlette import status

from api.v1.dependencies.services import RoomServiceDep
from api.v1.dependencies.studio import ValidStudioIdDep
from api.v1.dependencies.types import PathIntID
from exceptions.room import (
    RoomNotFoundException,
    RoomDoesNotExistInStudioException,
)
from models.room import Room
from schemas.room import RoomRead
from services.file import FileService
from services.room import RoomService


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


async def valid_studio_room_id(
    room_id: PathIntID, studio: ValidStudioIdDep, room_service: RoomServiceDep
) -> Room:
    try:
        room = await room_service.check_if_room_in_studio(room_id, studio.id)
    except RoomNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except RoomDoesNotExistInStudioException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return room


ValidStudioRoomIdDep = Annotated[Room, Depends(valid_studio_room_id)]
