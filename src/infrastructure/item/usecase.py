from abc import ABC

from src.infrastructure.item.repository import Repository as RepositoryABC


class UseCase[Repository: RepositoryABC](ABC):
    _repository: Repository

    def __init__(self, repository: type[Repository]):
        self._repository = repository()
