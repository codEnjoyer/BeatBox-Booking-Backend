from src.domain.models.base import IDBaseModel
from src.domain.models.repositories.orm.repository import ORMRepository
from src.infrastructure.item.usecases.delete import DeleteItemUseCase


class DeleteByIdUseCase[ID,
                        Model: IDBaseModel,
                        Repository: ORMRepository] \
            (DeleteItemUseCase[Repository]):
    _model: Model

    def __init__(self, model: Model, repository: type[Repository]):
        self._model = model
        super().__init__(repository)

    async def delete_by_id(self, id_: ID) -> None:
        await super().delete(self._model.id == id_)
