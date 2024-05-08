from src.domain.models.base import BaseModel
from src.domain.models.repositories.orm.repository import ORMRepository
from src.domain.schemas.base import BaseSchema
from src.infrastructure.item.usecases.create import CreateItemUseCase


class CreateUseCase[Model: BaseModel,
                    Schema: BaseSchema,
                    Repository: ORMRepository] \
            (CreateItemUseCase[Model, Schema, Repository]):
    ...