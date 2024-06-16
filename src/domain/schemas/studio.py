import datetime
from typing import Self, Annotated

from pydantic import (
    Field,
    HttpUrl,
    PositiveInt,
    field_validator,
    model_validator,
    field_serializer,
)
from pydantic_core.core_schema import SerializationInfo

from src.domain.schemas.base import BaseSchema

from src.domain.schemas.phone_number import RuPhoneNumber

StudioWorkingTime = Annotated[
    datetime.time,
    Field(
        examples=[
            "10:00:00+0500",
            datetime.time(
                hour=10, minute=0, second=0, tzinfo=datetime.timezone.utc
            ),
        ]
    ),
]


class BaseStudio(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(min_length=1, max_length=500)
    opening_at: StudioWorkingTime
    closing_at: StudioWorkingTime
    latitude: float = Field(gt=-90, le=90, examples=[0.0])
    longitude: float = Field(gt=-180, le=180, examples=[0.0])

    site: HttpUrl | None
    contact_phone_number: RuPhoneNumber | None = Field(examples=["79123456789"])
    # TODO: добавить валидацию соц. сетей
    tg: str | None
    vk: str | None
    whats_app: str | None

    @field_validator("opening_at", "closing_at")
    @classmethod
    def time_with_tz(cls, value: datetime.time) -> datetime.time:
        if value.tzinfo is None or value.tzinfo.utcoffset(None) is None:
            raise ValueError("time must be with timezone")
        return value

    @model_validator(mode="after")
    def closing_at_greater_than_opening_at(self) -> Self:
        if self.closing_at < self.opening_at:
            raise ValueError("closing_at must be greater than opening_at")
        return self

    @field_serializer("site")
    def url_to_string(self, value: HttpUrl, _: SerializationInfo) -> str:
        return value.unicode_string()


class StudioRead(BaseStudio):
    id: PositiveInt
    average_grade: float = Field(ge=0, le=5, examples=[4.4])


class StudioCreate(BaseStudio): ...


class StudioUpdate(BaseStudio): ...
