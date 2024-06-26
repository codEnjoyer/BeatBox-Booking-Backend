from fastapi import APIRouter

from api.v1.auth import router as auth_router
from api.v1.booking import router as booking_router
from api.v1.employee import router as employee_router
from api.v1.file import router as file_router
from api.v1.review import router as review_router
from api.v1.room import router as room_router
from api.v1.studio import router as studio_router
from api.v1.user import router as user_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(auth_router)
router.include_router(employee_router)
router.include_router(file_router)
router.include_router(review_router)
router.include_router(studio_router)
router.include_router(user_router)
router.include_router(room_router)
router.include_router(booking_router)
