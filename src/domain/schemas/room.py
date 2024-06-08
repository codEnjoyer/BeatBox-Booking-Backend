import uuid

from src.domain.schemas.base import BaseSchema


class BaseRoom(BaseSchema):
    name: str
    description: str


class RoomRead(BaseRoom):
    banner: str | None
    images: list[str] | None


class RoomCreate(BaseRoom):
    banner_id: uuid.UUID | None


class RoomUpdate(BaseRoom):
    banner_id: uuid.UUID | None
