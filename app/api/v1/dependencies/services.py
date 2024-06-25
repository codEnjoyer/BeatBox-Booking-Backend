from typing import Annotated

from fastapi import Depends

from app.domain.services.auth import AuthService
from app.domain.services.booking import BookingService
from app.domain.services.employee import EmployeeService
from app.domain.services.file import FileService
from app.domain.services.review import ReviewService
from app.domain.services.room import RoomService
from app.domain.services.studio import StudioService
from app.domain.services.user import UserService
from app.settings import auth_settings


def get_auth_service() -> AuthService:
    return AuthService(auth_settings.secret_auth_token)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
BookingServiceDep = Annotated[BookingService, Depends(BookingService)]
EmployeeServiceDep = Annotated[EmployeeService, Depends(EmployeeService)]
FileServiceDep = Annotated[FileService, Depends(FileService)]
ReviewServiceDep = Annotated[ReviewService, Depends(ReviewService)]
RoomServiceDep = Annotated[RoomService, Depends(RoomService)]
StudioServiceDep = Annotated[StudioService, Depends(StudioService)]
UserServiceDep = Annotated[UserService, Depends(UserService)]
