from typing import Tuple

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
