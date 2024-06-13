from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from src.api.dependencies.services import StudioServiceDep
from src.domain.exceptions.studio import StudioNotFoundException
from src.domain.models import Studio


async def valid_studio_id(
    studio_id: int, studio_service: StudioServiceDep
) -> Studio:
    try:
        studio = await studio_service.get_by_id(model_id=studio_id)
    except StudioNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return studio


ValidStudioIdDep = Annotated[Studio, Depends(valid_studio_id)]
