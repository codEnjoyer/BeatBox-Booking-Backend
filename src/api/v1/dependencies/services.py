from typing import Annotated

from fastapi import Depends

from src.domain.services.booking import BookingService
from src.domain.services.employee import EmployeeService
from src.domain.services.file import FileService
from src.domain.services.review import ReviewService
from src.domain.services.room import RoomService
from src.domain.services.studio import StudioService
from src.domain.services.user import UserService

BookingServiceDep = Annotated[BookingService, Depends(BookingService)]
EmployeeServiceDep = Annotated[EmployeeService, Depends(EmployeeService)]
FileServiceDep = Annotated[FileService, Depends(FileService)]
ReviewServiceDep = Annotated[ReviewService, Depends(ReviewService)]
RoomServiceDep = Annotated[RoomService, Depends(RoomService)]
StudioServiceDep = Annotated[StudioService, Depends(StudioService)]
UserServiceDep = Annotated[UserService, Depends(UserService)]
