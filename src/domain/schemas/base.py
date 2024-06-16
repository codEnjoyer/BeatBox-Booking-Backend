from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    AwareDatetime,
    PlainSerializer,
    Field,
)


def convert_datetime_to_iso_8601_with_tz(dt: datetime) -> str:
    print(dt.tzinfo)
    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


DatetimeTZ = Annotated[
    AwareDatetime,
    PlainSerializer(convert_datetime_to_iso_8601_with_tz, return_type=str),
    Field(examples=['2024-06-16T11:36:43+0000']),
]


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
