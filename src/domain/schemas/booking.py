from src.domain.schemas.base import BaseSchema
from src.domain.schemas.file import FileRead


class BaseBooking(BaseSchema):
    name: str
    description: str


class BookingRead(BaseBooking):
    banner: FileRead
    images: list[FileRead]


class BookingCreate(BaseBooking):
    banner_id: int | None


class BookingUpdate(BaseBooking):
    banner_id: int | None
