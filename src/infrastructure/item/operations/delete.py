from abc import ABC, abstractmethod

from src.infrastructure.item.operations.base import RepositoryOperation


class DeleteOperation[Item](RepositoryOperation, ABC):
    @abstractmethod
    async def delete(self,
                     *where) -> None:
        ...
