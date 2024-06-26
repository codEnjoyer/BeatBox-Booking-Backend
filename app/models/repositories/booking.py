from typing import override

from models import Booking
from models.repositories.SQLAlchemy import SQLAlchemyRepository
from schemas.booking import BookingCreate, BookingUpdate


class BookingRepository(
    SQLAlchemyRepository[Booking, BookingCreate, BookingUpdate]
):
    @override
    @property
    def model(self) -> type[Booking]:
        return Booking
