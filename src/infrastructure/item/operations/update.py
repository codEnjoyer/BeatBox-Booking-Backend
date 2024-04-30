from abc import ABC, abstractmethod

from src.infrastructure.item.operations.base import RepositoryOperation


class UpdateOperation[Item, UpdateSchema](RepositoryOperation, ABC):
    @abstractmethod
    async def update(self,
                     schema: UpdateSchema,
                     *where) -> list[Item]:
        ...
