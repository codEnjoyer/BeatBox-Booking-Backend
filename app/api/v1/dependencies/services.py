from typing import Annotated

from fastapi import Depends

from services.auth import AuthService
from services.booking import BookingService
from services.employee import EmployeeService
from services.file import FileService
from services.review import ReviewService
from services.room import RoomService
from services.studio import StudioService
from services.user import UserService
from settings.auth import auth_settings


def get_auth_service() -> AuthService:
    return AuthService(auth_settings.secret_token)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
BookingServiceDep = Annotated[BookingService, Depends(BookingService)]
EmployeeServiceDep = Annotated[EmployeeService, Depends(EmployeeService)]
FileServiceDep = Annotated[FileService, Depends(FileService)]
ReviewServiceDep = Annotated[ReviewService, Depends(ReviewService)]
RoomServiceDep = Annotated[RoomService, Depends(RoomService)]
StudioServiceDep = Annotated[StudioService, Depends(StudioService)]
UserServiceDep = Annotated[UserService, Depends(UserService)]
