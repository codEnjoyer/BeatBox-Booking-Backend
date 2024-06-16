import uuid
from typing import override


from src.domain.exceptions.room import (
    RoomNotFoundException,
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

    async def create_room_in_studio(
            self, studio_id: int, schema: RoomCreate
    ) -> Room:
        schema_dict = schema.model_dump()
        schema_dict["studio_id"] = studio_id
        created = await self._repository.create(schema_dict)
        return await self.get_by_id(created.id)

    @override
    async def update_by_id(self, room_id: int, schema: RoomUpdate) -> Room:
        updated = await super().update_by_id(room_id, schema)
        return await self.get_by_id(updated.id)

    async def check_if_room_in_studio(
            self, room_id: int, studio_id: int
    ) -> None:
        room = await self.get_by_id(room_id)
        if room.studio_id != studio_id:
            raise RoomDoesNotExistInStudioException()

    async def get_all_images(self, room_id: int) -> list[uuid.UUID]:
        return await self._repository.get_all_images_by_id(room_id=room_id)
