from typing import Annotated

from fastapi import Depends

from src.domain.services.studio import StudioService


def get_studio_service() -> StudioService:
    return StudioService()


StudioServiceDep = Annotated[StudioService, Depends(get_studio_service)]
