from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from src.api.v1.dependencies.auth import AuthenticatedUser
from src.api.v1.dependencies.services import ReviewServiceDep
from src.api.v1.dependencies.studio import ValidStudioIdDep
from src.domain.exceptions.review import ReviewNotFoundException
from src.domain.models import Review


async def valid_review_id(
    _: ValidStudioIdDep, review_id: int, review_service: ReviewServiceDep
) -> Review:
    try:
        review = await review_service.get_by_id(review_id)
    except ReviewNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return review


ValidReviewIdDep = Annotated[Review, Depends(valid_review_id)]


async def owned_review(
    review: ValidReviewIdDep, user: AuthenticatedUser
) -> Review:
    if review.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be owner of this review",
        )
    return review


OwnedReviewDep = Annotated[Review, Depends(owned_review)]
