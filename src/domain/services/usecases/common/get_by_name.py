from src.domain.models.base import BaseModel
from src.domain.models.repositories.orm.repository import ORMRepository
from src.infrastructure.item.usecases.read import GetOneItemUseCase


class GetByNameUseCase[TName,
                       Model: BaseModel,
                       Repository: ORMRepository] \
            (GetOneItemUseCase[Model, Repository]):
    _model: Model

    def __init__(self, model: Model, repository: type[Repository]):
        self._model = model
        super().__init__(repository)

    async def get_by_id(self, name: TName) -> Model:
        return await super().get_one(self._model.name == name)
