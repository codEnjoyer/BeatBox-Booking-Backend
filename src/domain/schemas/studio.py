from pydantic import AnyHttpUrl
from src.domain.schemas.base import BaseSchema
import datetime as dt

from src.domain.schemas.phone_number import PhoneNumber


class BaseStudio(BaseSchema):
    name: str
    description: str
    address: str
    opening_at: dt.time
    closing_at: dt.time
    latitude: float | None
    longitude: float | None
    site_url: AnyHttpUrl | None
    # TODO: при дампе url конвертировать в строку
    # бд не принимает Url при создании студии
    contact_phone_number: PhoneNumber | None
    tg: str | None
    vk: str | None
    whats_app: str | None


class StudioRead(BaseStudio):
    id: int
    average_grade: float


class StudioCreate(BaseStudio): ...


class StudioUpdate(BaseStudio): ...
