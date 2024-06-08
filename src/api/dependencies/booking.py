from src.domain.models.booking import Booking
from src.domain.schemas.booking import BookingRead


def convert_model_to_scheme(booking: Booking) -> BookingRead:
    return BookingRead(
        status=booking.status,
        name=booking.name,
        surname=booking.surname,
        starts_at=booking.starts_at,
        ends_at=booking.ends_at,
        room_id=booking.room_id,
        id=booking.id,
        user_id=booking.user_id,
    )
