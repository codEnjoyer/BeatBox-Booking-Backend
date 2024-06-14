import datetime

from pydantic import Field, HttpUrl, PositiveInt
from src.domain.schemas.base import BaseSchema

from src.domain.schemas.phone_number import PhoneNumber
from src.domain.schemas.room import RoomRead


class BaseStudio(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    # TODO: проверить поведение description
    description: str | None = Field(min_length=1)
    opening_at: datetime.time
    closing_at: datetime.time
    # TODO: opening_at < closing_at
    latitude: float
    longitude: float

    site: HttpUrl | None
    contact_phone_number: PhoneNumber | None
    # TODO: добавить валидацию соц. сетей
    tg: str | None
    vk: str | None
    whats_app: str | None


class StudioRead(BaseStudio):
    id: PositiveInt
    average_grade: float

    rooms: list[RoomRead]


class StudioCreate(BaseStudio): ...


class StudioUpdate(BaseStudio): ...
