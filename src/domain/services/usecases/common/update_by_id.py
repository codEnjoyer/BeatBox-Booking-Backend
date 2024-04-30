from src.domain.models.base import BaseModel
from src.domain.models.repositories.orm.repository import ORMRepository
from src.domain.schemas.base import BaseSchema
from src.infrastructure.item.usecases.update import UpdateItemUseCase


class UpdateByIdUseCase[ID,
                        Model: BaseModel,
                        Schema: BaseSchema,
                        Repository: ORMRepository] \
            (UpdateItemUseCase[Model, Schema, Repository]):
    _model: Model

    def __init__(self, model: Model, repository: type[Repository]):
        self._model = model
        super().__init__(repository)

    async def delete_by_id(self, id_: ID) -> None:
        await super().update(self._model.id == id_)
