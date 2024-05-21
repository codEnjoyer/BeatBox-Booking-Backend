import uuid

from src.domain.schemas.base import BaseSchema
from src.domain.schemas.file import FileBucketRead


class BaseRoom(BaseSchema):
    name: str
    description: str


class RoomRead(BaseRoom):
    banner: FileBucketRead | None
    images: list[FileBucketRead] | None


class RoomCreate(BaseRoom):
    banner_id: uuid.UUID | None


class RoomUpdate(BaseRoom):
    banner_id: uuid.UUID | None
