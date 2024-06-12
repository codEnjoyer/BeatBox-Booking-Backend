from src.domain.exceptions.base import ItemNotFoundException


class RoomNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Room"
