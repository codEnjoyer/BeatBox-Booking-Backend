from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.domain.exceptions.studio import StudioNotFoundException
from src.domain.services.auth import manager
from src.domain.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate
from src.domain.models.user import User
from src.domain.services.review import ReviewService
from src.domain.services.studio import StudioService

router = APIRouter(prefix="/studios", tags=["Review"])


@router.post("/{studio_id}/reviews", response_model=ReviewRead)
async def add_review(
    studio_id: int,
    schema: ReviewCreate,
    review_service: ReviewService = Depends(ReviewService),
    studio_service: StudioService = Depends(StudioService),
    user: User = Depends(manager),
) -> ReviewRead:
    try:
        studio = await studio_service.get_by_id(studio_id)
    except StudioNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Studio not found"
        )
    # try:
    #     room = await room_service.get_room_by_id(studio_id, schema.room_id)
    # except RoomNotFoundException: ## TODO: check room existence
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Invalid room"
    #     )

    review = await review_service.create(
        schema=schema, author_id=user.id
    )
    return review


@router.get("/{studio_id}/reviews", response_model=list[ReviewRead])
async def get_reviews(
    studio_id: int, service: ReviewService = Depends(ReviewService), offset: int = 0, limit: int = 100
) -> list[ReviewRead]:
    return await service.get_reviews_by_studio_id(
        studio_id=studio_id, offset=offset, limit=limit
    )


@router.patch("/{studio_id}/reviews/{review_id}", response_model=ReviewRead)
async def patch_review(
    studio_id: int,
    review_id: int,
    schema: ReviewUpdate,
    service: ReviewService = Depends(ReviewService),
    user: User = Depends(manager),
) -> ReviewRead:
    review = await service.patch_review(
        studio_id=studio_id,
        author_id=user.id,
        review_id=review_id,
        schema=schema,
    )
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not have review on this studio",
        )
    return ReviewRead(
        author_id=review.author_id,
        studio_id=review.studio_id,
        grade=review.grade,
        text=review.text,
    )
