from abc import ABC

from src.infrastructure.item.operations import (CreateOperation, GetOneOperation,
                                                GetAllOperation, UpdateOperation, \
                                                DeleteOperation)


class Repository[Item, CreateSchema, UpdateSchema] \
            (CreateOperation[Item, CreateSchema],
             GetOneOperation[Item],
             GetAllOperation[Item],
             UpdateOperation[Item, UpdateSchema],
             DeleteOperation[Item],
             ABC):
    ...
