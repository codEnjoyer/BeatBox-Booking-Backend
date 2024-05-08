from abc import ABC, abstractmethod

from src.infrastructure.item.operations.base import RepositoryOperation


class CreateOperation[Item, CreateSchema](RepositoryOperation, ABC):
    @abstractmethod
    async def create(self,
                     schema: CreateSchema) -> Item:
        ...
