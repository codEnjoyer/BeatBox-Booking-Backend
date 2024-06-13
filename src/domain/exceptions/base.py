from abc import abstractmethod

from sqlalchemy.exc import NoResultFound


class BBBException(Exception):
    message: str

    def __init__(self, message: str = "Service error"):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class ItemNotFoundException(BBBException, NoResultFound):
    @property
    @abstractmethod
    def item_name(self) -> str: ...

    def __init__(self):
        super().__init__(f"{self.item_name} not found")


class BadDataException(BBBException):
    def __init__(self, message: str = "Bad data"):
        super().__init__(message)
