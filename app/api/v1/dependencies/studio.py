from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from api.v1.dependencies.auth import AuthenticatedEmployee
from api.v1.dependencies.services import StudioServiceDep
from api.v1.dependencies.types import PathIntID
from exceptions.studio import StudioNotFoundException
from models import Studio, Employee


async def valid_studio_id(
    studio_id: PathIntID, studio_service: StudioServiceDep
) -> Studio:
    try:
        studio = await studio_service.get_by_id(studio_id)
    except StudioNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return studio


ValidStudioIdDep = Annotated[Studio, Depends(valid_studio_id)]


async def studio_employee(
    studio: ValidStudioIdDep, employee: AuthenticatedEmployee
) -> Employee:
    if not employee.studio_id == studio.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be employee in this studio",
        )
    return employee


StudioEmployeeDep = Annotated[Employee, Depends(studio_employee)]
