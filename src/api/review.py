from fastapi import APIRouter

from src.api.dependencies.services import ReviewServiceDep
from src.api.dependencies.auth import AuthenticatedUser
from src.domain.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/studios", tags=["Review"])


@router.post("/{studio_id}/reviews", response_model=ReviewRead)
async def add_review(
    studio_id: int,
    schema: ReviewCreate,
    service: ReviewServiceDep,
    user: AuthenticatedUser,
) -> ReviewRead:
    review = await service.create(
        schema=schema, author_id=user.id, studio_id=studio_id
    )
    return review


@router.get("/{studio_id}/reviews", response_model=list[ReviewRead])
async def get_reviews(
    studio_id: int, service: ReviewServiceDep, offset: int = 0, limit: int = 100
) -> list[ReviewRead]:
    reviews = await service.get_reviews_by_studio_id(
        studio_id=studio_id, offset=offset, limit=limit
    )
    return reviews


@router.put("/{studio_id}/reviews/{review_id}", response_model=ReviewRead)
async def patch_review(
    studio_id: int,
    review_id: int,
    schema: ReviewUpdate,
    service: ReviewServiceDep,
    user: AuthenticatedUser,
) -> ReviewRead:
    review = await service.patch_review(
        studio_id=studio_id,
        author_id=user.id,
        review_id=review_id,
        schema=schema,
    )
    return review
