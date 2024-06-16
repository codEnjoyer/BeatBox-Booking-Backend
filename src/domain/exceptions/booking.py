from src.domain.exceptions.base import ItemNotFoundException, BadDataException


class BookingNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Booking"


class MustBookWithinOneDayException(BadDataException):
    def __init__(self):
        super().__init__("Booking must be within one day")


class MustBookWithinStudioWorkingTimeException(BadDataException):
    def __init__(self):
        super().__init__("Booking must be within studio working time")


class SlotAlreadyBookedException(BadDataException):
    def __init__(self):
        super().__init__("Slot already booked")
