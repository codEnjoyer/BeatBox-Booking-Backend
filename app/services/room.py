import uuid
from typing import override

from sqlalchemy.exc import NoResultFound

from exceptions.room import (
    RoomNotFoundException,
    RoomDoesNotExistInStudioException,
)
from models import Room
from models.repositories.room import RoomRepository
from schemas.room import RoomCreate, RoomUpdate
from services.base import ModelService


class RoomService(ModelService[RoomRepository, Room, RoomCreate, RoomUpdate]):
    def __init__(self):
        super().__init__(RoomRepository(), RoomNotFoundException)

    async def get_all_in_studio(self, studio_id: int) -> list[Room]:
        rooms = await self._repository.get_all(
            self.model.studio_id == studio_id,
        )
        return rooms

    async def create_room_in_studio(
        self, studio_id: int, schema: RoomCreate
    ) -> Room:
        schema_dict = schema.model_dump()
        schema_dict["studio_id"] = studio_id
        created = await self._repository.create(schema_dict)
        return await self.get_by_id(created.id)

    async def create_if_not_exists(
        self, studio_id: int, schema: RoomCreate
    ) -> Room:
        try:
            return await self._repository.get_one(
                self.model.name == schema.name,
                self.model.studio_id == studio_id,
            )
        except NoResultFound:
            return await self.create_room_in_studio(studio_id, schema)

    @override
    async def update_by_id(self, model_id: int, schema: RoomUpdate) -> Room:
        updated = await super().update_by_id(model_id, schema)
        return await self.get_by_id(updated.id)

    async def check_if_room_in_studio(
        self, room_id: int, studio_id: int
    ) -> Room:
        room = await self.get_by_id(room_id)
        if room.studio_id != studio_id:
            raise RoomDoesNotExistInStudioException()
        return room

    async def get_all_images(self, room_id: int) -> list[uuid.UUID]:
        return await self._repository.get_all_images_by_id(room_id=room_id)
