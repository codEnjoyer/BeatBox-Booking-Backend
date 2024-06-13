import uuid

from fastapi import HTTPException
from sqlalchemy import ColumnElement
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.domain.exceptions.room import (
    RoomNotFoundException,
    RoomWithSameNameAlreadyExistsException,
)
from src.domain.models import Room
from src.domain.models.repositories.room import RoomRepository
from src.domain.schemas.room import RoomCreate, RoomUpdate
from src.domain.services.base import ModelService


class RoomService(ModelService[RoomRepository, Room, RoomCreate, RoomUpdate]):
    def __init__(self):
        super().__init__(RoomRepository(), RoomNotFoundException)

    async def is_room_exist(self, *where: ColumnElement[bool]) -> bool:
        # TODO: переделать
        try:
            await self._repository.get_one(*where)
        except NoResultFound:
            return False
        return True

    async def create_room_in_studio(
        self, studio_id: int, schema: RoomCreate
    ) -> Room:
        if await self.is_room_exist(
            self.model.name == schema.name, self.model.studio_id == studio_id
        ):
            raise RoomWithSameNameAlreadyExistsException()
        schema_dict = schema.model_dump()
        schema_dict["studio_id"] = studio_id
        try:
            return await self._repository.create(schema_dict)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File with that id not found",
            )

    async def get_all_images(self, room_id: int) -> list[uuid.UUID]:
        return await self._repository.get_all_images_by_id(room_id=room_id)
