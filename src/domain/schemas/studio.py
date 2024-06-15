import datetime
from typing import Self, Any

from pydantic import (
    Field,
    HttpUrl,
    PositiveInt,
    field_validator,
    model_validator,
    field_serializer,
)
from pydantic_core.core_schema import ValidationInfo, SerializationInfo

from src.domain.schemas.base import BaseSchema

from src.domain.schemas.phone_number import PhoneNumber


class BaseStudio(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    # TODO: проверить поведение description
    description: str | None = Field(min_length=1)
    opening_at: datetime.time
    closing_at: datetime.time
    # TODO: opening_at/closing_at привести к HH:MM+TZ
    latitude: float = Field(gt=-90, le=90)
    longitude: float = Field(gt=-180, le=180)

    site: HttpUrl | None
    contact_phone_number: PhoneNumber | None
    # TODO: добавить валидацию соц. сетей
    tg: str | None
    vk: str | None
    whats_app: str | None

    @model_validator(mode="after")
    def closing_at_greater_than_opening_at(self) -> Self:
        if self.closing_at < self.opening_at:
            raise ValueError("closing_at must be greater than opening_at")
        return self

    @field_serializer("site")
    def url_to_string(self, value: HttpUrl, _: SerializationInfo) -> str:
        return value.unicode_string()

    # @field_serializer("opening_at", "closing_at")
    # def time_to_string(self, value: datetime.time, _: SerializationInfo)
    # -> str:
    #     return value.strftime("%H:%M%z")


class StudioRead(BaseStudio):
    id: PositiveInt
    average_grade: float

    @field_validator("opening_at", "closing_at", mode="before")
    @classmethod
    def time_with_timezone(cls, value: Any, _: ValidationInfo) -> datetime.time:
        if not isinstance(value, str):
            raise ValueError("time must be parsed from string")
        date_time = datetime.datetime.strptime(value, "%H:%M%z")
        return datetime.time(
            hour=date_time.hour,
            minute=date_time.minute,
            tzinfo=date_time.tzinfo,
        )


class StudioCreate(BaseStudio):
    @field_validator("opening_at", "closing_at", mode="before")
    @classmethod
    def time_with_timezone(cls, value: Any, _: ValidationInfo) -> datetime.time:
        if not isinstance(value, str):
            raise ValueError("time must be parsed from string")
        date_time = datetime.datetime.strptime(value, "%H:%M%z")
        return datetime.time(
            hour=date_time.hour,
            minute=date_time.minute,
            tzinfo=date_time.tzinfo,
        )


class StudioUpdate(BaseStudio): ...
