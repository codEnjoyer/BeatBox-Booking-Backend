from pydantic import Field

from src.domain.schemas.base import BaseSchema, IntID


class BaseAdditionalService(BaseSchema):
    name: str = Field(min_length=1)
    # TODO: проверить поведение description
    description: str | None = Field(min_length=1)


class AdditionalServiceRead(BaseAdditionalService):
    id: IntID


class AdditionalServiceCreate(BaseAdditionalService): ...
