import uuid

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from starlette import status

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
        try:
            model = await self._repository.get_all(
                self.model.studio_id == studio_id,
                options=(
                    selectinload(self.model.additional_services),
                    selectinload(self.model.bookings),
                ),
            )
        except NoResultFound as e:
            raise self._not_found_exception from e
        return model

    async def get_by_name_in_studio(
        self,
        name: str,
        studio_id: int,
    ) -> Room:
        try:
            model = await self._repository.get_one(
                self.model.name == name,
                self.model.studio_id == studio_id,
                options=(
                    selectinload(self.model.additional_services),
                    selectinload(self.model.bookings),
                ),
            )
        except NoResultFound as e:
            raise self._not_found_exception from e
        return model

    async def create_room_in_studio(
        self, studio_id: int, schema: RoomCreate
    ) -> Room:
        if await self.is_room_with_name_exist_in_studio(schema.name, studio_id):
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

    async def is_room_with_name_exist_in_studio(
        self, name: str, studio_id: int
    ) -> bool:
        try:
            await self.get_by_name_in_studio(name, studio_id)
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
