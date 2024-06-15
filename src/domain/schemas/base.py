from datetime import datetime

from pydantic import BaseModel, ConfigDict


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: convert_datetime_to_iso_8601_with_z_suffix},
    )
