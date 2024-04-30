from src.domain.models.base import BaseModel
from src.domain.models.repositories.orm.repository import ORMRepository
from src.infrastructure.item.usecases.read import GetAllItemsUseCase


class GetAllUseCase[Model: BaseModel,
                    Repository: ORMRepository] \
            (GetAllItemsUseCase[Model, Repository]):
    ...
