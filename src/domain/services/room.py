import uuid

from fastapi import HTTPException
from starlette import status

from src.domain.exceptions.room import RoomNotFoundException
from src.domain.models import Room
from src.domain.models.repositories.room import RoomRepository
from src.domain.schemas.room import RoomCreate, RoomUpdate
from src.domain.services.base import ModelService


class RoomService(ModelService[RoomRepository, Room, RoomCreate, RoomUpdate]):
    def __init__(self):
        super().__init__(RoomRepository(), RoomNotFoundException)

    async def get(self, room_id: int) -> Room:
        room = await self._repository.get_one(self._model.id == room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room with that id not found",
            )
        return room

    async def create(self, schema: RoomCreate, **kwargs) -> Room:
        studio_id = kwargs.get("studio_id")
        if await self._repository.is_room_exist(
            self._model.name == schema.name, self._model.studio_id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room with same name already exists",
            )

        await self._repository.check_employee_permissions(
            user_id=kwargs.get("user_id"), studio_id=studio_id
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

    async def delete(self, room_id: int, studio_id: int, user_id: int) -> None:
        if not await self._repository.is_room_exist(
            self._model.id == room_id, self._model.studio_id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Studio with that name not found",
            )

        await self._repository.check_employee_permissions(
            user_id=user_id, studio_id=studio_id
        )

        room: Room = await self._repository.get(
            user_id,
            self._model.id == room_id,
            self._model.studio_id == studio_id,
        )

        return await self._repository.delete(self._model.id == room.id)

    async def update(
        self, room_id: int, studio_id: int, user_id: int, schema: RoomUpdate
    ) -> Room:
        if not await self._repository.is_room_exist(
            self._model.id == room_id, self._model.studio_id == studio_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Studio with that name not found",
            )

        await self._repository.check_employee_permissions(
            user_id=user_id, studio_id=studio_id
        )

        room: Room = await self._repository.get(
            user_id, self._model.id == studio_id
        )

        return await self._repository.update_one(
            schema, self._model.id == room.id
        )

    async def get_all_images(self, room_id: int) -> list[uuid.UUID]:
        return await self._repository.get_all_images_by_id(room_id=room_id)