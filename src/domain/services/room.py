import uuid

from fastapi import HTTPException
from sqlalchemy import ColumnElement
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.domain.exceptions.room import RoomNotFoundException
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

    async def create(self, schema: RoomCreate, **kwargs) -> Room:
        studio_id = kwargs.get("studio_id")
        if await self.is_room_exist(
            self.model.name == schema.name, self.model.studio_id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room with same name already exists",
            )

        if not await self._repository.is_working_in_studio(
            kwargs.get("employee_id"), studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid permissions",
            )

        studio_dict = {
            "name": schema.name,
            "description": schema.description,
            "banner_id": schema.banner_id,
            "studio_id": studio_id,
        }
        try:
            return await self._repository.create(studio_dict)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File with that id not found",
            )

    async def delete(
        self, room_id: int, studio_id: int, employee_id: int
    ) -> None:
        if not await self._repository.is_working_in_studio(
            employee_id, studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid permissions",
            )

        return await self._repository.delete(self.model.id == room_id)

    async def update(
        self, room_id: int, studio_id: int, employee_id: int, schema: RoomUpdate
    ) -> Room:
        if not await self._repository.is_working_in_studio(
            employee_id, studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid permissions",
            )

        return await self.update_by_id(schema, room_id)

    async def get_all_images(self, room_id: int) -> list[uuid.UUID]:
        return await self._repository.get_all_images_by_id(room_id=room_id)
