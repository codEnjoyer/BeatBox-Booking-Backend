from typing import override

from src.domain.models import Booking
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.booking import BookingCreate, BookingUpdate


class BookingRepository(
    SQLAlchemyRepository[Booking, BookingCreate, BookingUpdate]
):
    @override
    @property
    def model(self) -> type[Booking]:
        return Booking
