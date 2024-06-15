from typing import Annotated

from fastapi import Depends

from src.domain.services.auth import AuthService
from src.domain.services.booking import BookingService
from src.domain.services.employee import EmployeeService
from src.domain.services.file import FileService
from src.domain.services.review import ReviewService
from src.domain.services.room import RoomService
from src.domain.services.studio import StudioService
from src.domain.services.user import UserService
from src.settings import auth_settings


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
