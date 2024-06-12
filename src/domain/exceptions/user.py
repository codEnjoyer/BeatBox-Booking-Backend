from src.domain.exceptions.base import ItemNotFoundException


class UserNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "User"
