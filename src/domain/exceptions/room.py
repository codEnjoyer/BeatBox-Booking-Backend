from src.domain.exceptions.base import ItemNotFoundException, BadDataException


class RoomNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Room"


class RoomWithSameNameAlreadyExistsException(BadDataException):
    def __init__(self):
        super().__init__("Room with same name already exists")


class RoomDoesNotExistInStudioException(BadDataException):
    def __init__(self):
        super().__init__("Room does not exist in studio")
