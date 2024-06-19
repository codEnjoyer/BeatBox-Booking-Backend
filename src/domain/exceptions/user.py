from src.domain.exceptions.base import ItemNotFoundException, BadDataException


class UserNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "User"


class EmailAlreadyTakenException(BadDataException):
    def __init__(self):
        super().__init__("Email already taken")


class NicknameAlreadyTakenException(BadDataException):
    def __init__(self):
        super().__init__("Nickname already taken")
