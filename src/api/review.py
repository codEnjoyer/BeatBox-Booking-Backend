from fastapi import APIRouter

from src.api.dependencies.review import OwnedReviewDep
from src.api.dependencies.services import ReviewServiceDep
from src.api.dependencies.auth import AuthenticatedUser
from src.api.dependencies.studio import ValidStudioIdDep
from src.api.dependencies.types import QueryOffset, QueryLimit
from src.domain.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(tags=["Review"])


@router.get("/studios/{studio_id}/reviews", response_model=list[ReviewRead])
async def get_studio_reviews(
    studio: ValidStudioIdDep,
    service: ReviewServiceDep,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[ReviewRead]:
    reviews = await service.get_studio_reviews(
        studio.id, offset=offset, limit=limit
    )
    return reviews


# TODO: get room reviews?


@router.post("/studios/{studio_id}/reviews", response_model=ReviewRead)
async def post_review_on_studio(
    studio: ValidStudioIdDep,
    schema: ReviewCreate,
    review_service: ReviewServiceDep,
    user: AuthenticatedUser,
) -> ReviewRead:
    review = await review_service.add_new_from_user(schema, user.id, studio.id)
    return review


@router.put("/studios/{studio_id}/reviews/{review_id}", response_model=ReviewRead)
async def update_my_studio_review(
    review: OwnedReviewDep,
    schema: ReviewUpdate,
    review_service: ReviewServiceDep,
    _: AuthenticatedUser,
) -> ReviewRead:
    return await review_service.update_by_id(schema, review.id)


# TODO: добавить удаление
