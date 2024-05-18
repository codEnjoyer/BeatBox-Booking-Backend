from typing import Annotated

from fastapi import Depends

from src.domain.services.review import ReviewService


def get_file_service() -> ReviewService:
    return ReviewService()


ReviewServiceDep = Annotated[ReviewService, Depends(get_file_service)]
