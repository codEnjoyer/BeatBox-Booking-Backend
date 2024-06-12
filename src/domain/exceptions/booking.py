from src.domain.exceptions.base import ItemNotFoundException


class BookingNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Booking"
