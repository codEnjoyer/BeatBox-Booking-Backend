from fastapi import APIRouter

from src.api.dependencies.review import OwnedReviewDep
from src.api.dependencies.services import ReviewServiceDep
from src.api.dependencies.auth import AuthenticatedUser
from src.api.dependencies.studio import ValidStudioIdDep
from src.domain.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(tags=["Review"])


@router.post("/studios/{studio_id}/reviews", response_model=ReviewRead)
async def add_review(
    studio: ValidStudioIdDep,
    schema: ReviewCreate,
    review_service: ReviewServiceDep,
    user: AuthenticatedUser,
) -> ReviewRead:
    review = await review_service.add_new_from_user(schema, user.id, studio.id)
    return review


@router.get("/{studio_id}/reviews", response_model=list[ReviewRead])
async def get_studio_reviews(
    studio: ValidStudioIdDep,
    service: ReviewServiceDep,
    offset: int = 0,
    limit: int = 100,
) -> list[ReviewRead]:
    reviews = await service.get_studio_reviews(
        studio.id, offset=offset, limit=limit
    )
    return reviews


@router.put("/{studio_id}/reviews/{review_id}", response_model=ReviewRead)
async def update_studio_review(
    review: OwnedReviewDep,
    schema: ReviewUpdate,
    review_service: ReviewServiceDep,
    _: AuthenticatedUser,
) -> ReviewRead:
    return await review_service.update_by_id(schema, review.id)


# TODO: добавить удаление
