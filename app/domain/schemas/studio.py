import datetime
from typing import Self, Annotated

from pydantic import (
    Field,
    HttpUrl,
    field_validator,
    model_validator,
    field_serializer,
)
from pydantic_core.core_schema import SerializationInfo

from app.domain.schemas.base import BaseSchema, IntID, NonEmptyString

from app.domain.schemas.phone_number import RuPhoneNumber

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

TgLink = Annotated[
    NonEmptyString,
    Field(
        examples=["https://t.me/Moz-Art_school"],
        # https://regex101.com/r/XkxTty/1
        pattern=r"^(?:|(https?:\/\/)?(|www)[.]?((t|telegram)\.me)\/)"
        r"[a-zA-Z0-9_]{5,32}$",
        max_length=100
    ),
]

VkLink = Annotated[
    NonEmptyString,
    Field(
        examples=["https://vk.com/mozartekb"],
        pattern=r"^(?:https?:\/\/)?(?:www\.)?vk\.com\/(.*)\/?$",
        max_length=100
    ),
]

WhatsAppLink = Annotated[
    NonEmptyString,
    Field(
        examples=["https://wa.me/79025026723"],
        pattern=r"^(?:https?:\/\/)?(?:www\.)?wa\.me\/(79\d{9})\/?$",
        max_length=100
    ),
]


class BaseStudio(BaseSchema):
    name: Annotated[NonEmptyString, Field(max_length=100)]
    description: Annotated[NonEmptyString, Field(max_length=1024)] | None
    opening_at: StudioWorkingTime
    closing_at: StudioWorkingTime
    latitude: float = Field(gt=-90, le=90, examples=[0.0])
    longitude: float = Field(gt=-180, le=180, examples=[0.0])

    site: HttpUrl | None
    contact_phone_number: RuPhoneNumber | None = Field(examples=["79123456789"])
    tg: TgLink | None
    vk: VkLink | None
    whats_app: WhatsAppLink | None

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
    id: IntID
    average_grade: float = Field(ge=0, le=5, examples=[4.4])


class StudioCreate(BaseStudio): ...


class StudioUpdate(BaseStudio): ...
