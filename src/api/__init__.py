from .auth import router as auth_router
from .studio import router as studio_router
from .user import router as user_router
from .file import router as file_router
from .review import router as review_router

__all__ = [
    "auth_router",
    "studio_router",
    "user_router",
    "file_router",
    "review_router",
]
