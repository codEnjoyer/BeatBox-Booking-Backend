from abc import ABC, abstractmethod


class Repository[Item, CreateSchema, UpdateSchema](ABC):
    _model: type[Item]

    @property
    def model(self) -> type[Item]:
        return self._model

    def __init__(self, model: type[Item]):
        self._model = model

    @abstractmethod
    async def create(self,
                     schema: CreateSchema) -> Item:
        ...

    @abstractmethod
    async def get_all(self,
                      *where,
                      offset: int = 0,
                      limit: int = 100) -> list[Item]:
        ...

    @abstractmethod
    async def get_one(self,
                      *where) -> Item | None:
        ...

    @abstractmethod
    async def update(self,
                     schema: UpdateSchema,
                     *where) -> list[Item]:
        ...

    @abstractmethod
    async def delete(self,
                     *where) -> None:
        ...
