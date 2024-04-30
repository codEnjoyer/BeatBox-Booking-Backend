from abc import ABC

from infrastructure.repository import Repository as RepositoryABC


class Service[Repository: RepositoryABC](ABC):
    _repository: Repository

    def __init__(self, repository: type[Repository]):
        self._repository = repository()
