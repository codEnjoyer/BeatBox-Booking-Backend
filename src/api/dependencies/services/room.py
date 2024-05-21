from typing import Annotated

from fastapi import Depends

from src.domain.services.room import RoomService


def get_room_service() -> RoomService:
    return RoomService()


RoomServiceDep = Annotated[RoomService, Depends(get_room_service)]
