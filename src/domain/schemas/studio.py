from src.domain.schemas.base import BaseSchema
import datetime as dt


class BaseStudio(BaseSchema):
    name: str
    description: str
    address: str
    opening_at: dt.datetime
    closing_at: dt.datetime
    latitude: float | None
    longitude: float | None
    site_url: str | None
    contact_phone_number: str | None
    tg: str | None
    vk: str | None
    whats_app: str | None


class StudioRead(BaseStudio): ...


class StudioCreate(BaseStudio): ...


class StudioUpdate(BaseStudio): ...
