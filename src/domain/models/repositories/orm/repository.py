from src.domain.models.base import BaseModel
from src.domain.models.repositories.orm.operations import (ORMCreate, ORMDelete, ORMReadOne,
                                                           ORMReadAll, ORMUpdate)
from src.domain.schemas.base import BaseSchema
from src.infrastructure.item.repository import Repository


class ORMRepository[Model: BaseModel,
                    CreateSchema: BaseSchema,
                    UpdateSchema: BaseSchema] \
            (Repository[Model, CreateSchema, UpdateSchema],
             ORMCreate[Model, CreateSchema],
             ORMReadOne[Model],
             ORMReadAll[Model],
             ORMUpdate[Model, UpdateSchema],
             ORMDelete[Model]):

    def __init__(self, model: type[Model]):
        super().__init__(model)
