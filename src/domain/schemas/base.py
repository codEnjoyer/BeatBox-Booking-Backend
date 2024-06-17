from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    AwareDatetime,
    PlainSerializer,
    Field,
    PositiveInt,
)


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


def convert_datetime_to_iso_8601_with_tz(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


DatetimeTZ = Annotated[
    AwareDatetime,
    PlainSerializer(convert_datetime_to_iso_8601_with_tz, return_type=str),
    Field(examples=['2024-06-16T11:00:00+0500']),
]
IntID = Annotated[PositiveInt, Field(examples=[1])]
NonEmptyString = Annotated[str, Field(min_length=1)]
