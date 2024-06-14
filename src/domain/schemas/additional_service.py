from pydantic import PositiveInt, Field

from src.domain.schemas.base import BaseSchema


class BaseAdditionalService(BaseSchema):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)


class AdditionalServiceRead(BaseAdditionalService):
    id: PositiveInt


class AdditionalServiceCreate(BaseAdditionalService): ...
