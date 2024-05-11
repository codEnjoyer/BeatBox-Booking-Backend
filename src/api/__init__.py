from .auth import router as auth_router
from .studio import router as studio_router
from .user import router as user_router

__all__ = ["auth_router",
           "studio_router",
           "user_router"]
