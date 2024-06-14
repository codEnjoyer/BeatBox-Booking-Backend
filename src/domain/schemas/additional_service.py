from pydantic import PositiveInt, Field

from src.domain.schemas.base import BaseSchema


class BaseAdditionalService(BaseSchema):
    name: str = Field(min_length=1)
    # TODO: проверить поведение description
    description: str | None = Field(min_length=1)


class AdditionalServiceRead(BaseAdditionalService):
    id: PositiveInt


class AdditionalServiceCreate(BaseAdditionalService): ...
