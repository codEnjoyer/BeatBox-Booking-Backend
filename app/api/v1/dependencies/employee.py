from typing import Annotated

from fastapi import HTTPException, status, Depends

from api.v1.dependencies.auth import AuthenticatedUser
from api.v1.dependencies.services import EmployeeServiceDep
from api.v1.dependencies.studio import ValidStudioIdDep
from api.v1.dependencies.types import PathIntID
from exceptions.employee import EmployeeNotFoundException
from models import User, Employee


def can_manage_studio(
    studio: ValidStudioIdDep, user: AuthenticatedUser
) -> User:
    if not user.can_manage_studio(studio.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    return user


StudioManagerDep = Annotated[User, Depends(can_manage_studio)]


async def valid_employee_id(
    employee_id: PathIntID, employee_service: EmployeeServiceDep
) -> Employee:
    try:
        employee = await employee_service.get_by_id(employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    return employee


ValidEmployeeIdDep = Annotated[Employee, Depends(valid_employee_id)]
