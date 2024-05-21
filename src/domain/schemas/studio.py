from pydantic import HttpUrl

from src.domain.schemas.base import BaseSchema
import datetime as dt

from src.domain.schemas.user import PhoneNumber


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
    tg: HttpUrl | None
    vk: HttpUrl | None
    whats_app: HttpUrl | None


class StudioRead(BaseStudio):
    pass


class StudioCreate(BaseStudio):
    pass


class StudioUpdate(BaseStudio):
    pass
