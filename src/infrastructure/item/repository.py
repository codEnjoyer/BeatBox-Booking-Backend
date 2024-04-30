from abc import ABC

from src.infrastructure.item.operations import CreateOperation, GetOperation, UpdateOperation, \
    DeleteOperation


class Repository[Item, CreateSchema, UpdateSchema] \
            (CreateOperation[Item, CreateSchema],
             GetOperation[Item],
             UpdateOperation[Item, UpdateSchema],
             DeleteOperation[Item],
             ABC):
    ...
