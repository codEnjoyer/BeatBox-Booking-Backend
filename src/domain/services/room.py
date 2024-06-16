import uuid
from typing import override

from sqlalchemy.exc import NoResultFound

from src.domain.exceptions.room import (
    RoomNotFoundException,
    RoomWithSameNameAlreadyExistsException,
    RoomDoesNotExistInStudioException,
)
from src.domain.models import Room
from src.domain.models.repositories.room import RoomRepository
from src.domain.schemas.room import RoomCreate, RoomUpdate
from src.domain.services.base import ModelService


class RoomService(ModelService[RoomRepository, Room, RoomCreate, RoomUpdate]):
    def __init__(self):
        super().__init__(RoomRepository(), RoomNotFoundException)

    async def get_all_in_studio(self, studio_id: int) -> list[Room]:
        rooms = await self._repository.get_all(
            self.model.studio_id == studio_id,
        )
        return rooms

    async def get_by_name(
        self, name: str, *, studio_id: int | None = None
    ) -> Room:
        where = [self.model.name == name]
        if studio_id:
            where.append(self.model.studio_id == studio_id)
        try:
            room = await self._repository.get_one(*where)
        except NoResultFound as e:
            raise self._not_found_exception from e
        return room

    async def create_room_in_studio(
        self, studio_id: int, schema: RoomCreate
    ) -> Room:
        if await self.is_room_with_name_exist_in_studio(schema.name, studio_id):
            raise RoomWithSameNameAlreadyExistsException()

        schema_dict = schema.model_dump()
        schema_dict["studio_id"] = studio_id
        created = await self._repository.create(schema_dict)
        return await self.get_by_id(created.id)

    @override
    async def update_by_id(self, room_id: int, schema: RoomUpdate) -> Room:
        updated = await super().update_by_id(room_id, schema)
        return await self.get_by_id(updated.id)

    async def is_room_with_name_exist_in_studio(
        self, name: str, studio_id: int
    ) -> bool:
        try:
            await self.get_by_name(name, studio_id=studio_id)
        except RoomNotFoundException:
            return False
        return True

    async def check_if_room_in_studio(
        self, room_id: int, studio_id: int
    ) -> None:
        room = await self.get_by_id(room_id)
        if room.studio_id != studio_id:
            raise RoomDoesNotExistInStudioException()

    async def get_all_images(self, room_id: int) -> list[uuid.UUID]:
        return await self._repository.get_all_images_by_id(room_id=room_id)
