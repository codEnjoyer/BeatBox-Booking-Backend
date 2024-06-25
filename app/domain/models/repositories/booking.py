from typing import override

from app.domain.models import Booking
from app.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from app.domain.schemas.booking import BookingCreate, BookingUpdate


class BookingRepository(
    SQLAlchemyRepository[Booking, BookingCreate, BookingUpdate]
):
    @override
    @property
    def model(self) -> type[Booking]:
        return Booking
