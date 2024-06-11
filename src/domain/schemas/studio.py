from pydantic import HttpUrl
from src.domain.schemas.base import BaseSchema
import datetime as dt

from src.domain.schemas.phone_number import PhoneNumber


class BaseStudio(BaseSchema):
    name: str
    description: str
    address: str
    opening_at: dt.datetime
    closing_at: dt.datetime
    latitude: float | None
    longitude: float | None
    site_url: HttpUrl | None
    contact_phone_number: PhoneNumber | None
    tg: str | None
    vk: str | None
    whats_app: str | None


class StudioRead(BaseStudio):
    id: int
    ...


class StudioCreate(BaseStudio):
    ...


class StudioUpdate(BaseStudio):
    ...
