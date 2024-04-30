from src.domain.models.base import BaseModel
from src.domain.models.repositories.orm.operations import ORMCreate, ORMDelete, ORMRead, ORMUpdate
from src.domain.schemas.base import BaseSchema
from src.infrastructure.item.repository import Repository


class ORMRepository[Model: BaseModel,
                    CreateSchema: BaseSchema,
                    UpdateSchema: BaseSchema] \
            (Repository[Model, CreateSchema, UpdateSchema],
             ORMCreate[Model, CreateSchema],
             ORMRead[Model],
             ORMUpdate[Model, UpdateSchema],
             ORMDelete[Model]):

    def __init__(self, model: type[Model]):
        super().__init__(model)
