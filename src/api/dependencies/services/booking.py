from typing import Annotated

from fastapi import Depends

from src.domain.services.booking import BookingService


def get_booking_service() -> BookingService:
    return BookingService()


BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]
