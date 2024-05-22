from .auth import router as auth_router
from .employee import router as employee_router
from .file import router as file_router
from .review import router as review_router
from .studio import router as studio_router
from .user import router as user_router
from .room import router as room_router
from .booking import router as booking_router

__all__ = [
    "auth_router",
    "employee_router",
    "file_router",
    "review_router",
    "studio_router",
    "user_router",
    "room_router",
    "booking_router",
]
