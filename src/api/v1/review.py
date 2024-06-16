from fastapi import APIRouter
from starlette import status

from src.api.v1.dependencies.review import OwnedReviewDep
from src.api.v1.dependencies.room import ValidStudioRoomNameDep
from src.api.v1.dependencies.services import ReviewServiceDep
from src.api.v1.dependencies.auth import AuthenticatedUser
from src.api.v1.dependencies.studio import ValidStudioIdDep
from src.api.v1.dependencies.types import QueryOffset, QueryLimit
from src.domain.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(tags=["Review"])


@router.get("/studios/{studio_id}/reviews", response_model=list[ReviewRead])
async def get_studio_reviews(
    studio: ValidStudioIdDep,
    review_service: ReviewServiceDep,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[ReviewRead]:
    reviews = await review_service.get_from_studio(
        studio.id, offset=offset, limit=limit
    )
    return reviews


@router.get(
    "/studios/{studio_id}/rooms/{room_name}/reviews",
    response_model=list[ReviewRead],
)
async def get_room_reviews(
    room: ValidStudioRoomNameDep,
    review_service: ReviewServiceDep,
    offset: QueryOffset = 0,
    limit: QueryLimit = 100,
) -> list[ReviewRead]:
    reviews = await review_service.get_from_room(
        room.id, offset=offset, limit=limit
    )
    return reviews


@router.post("/studios/{studio_id}/reviews", response_model=ReviewRead)
async def post_review_on_studio(
    studio: ValidStudioIdDep,
    schema: ReviewCreate,
    review_service: ReviewServiceDep,
    user: AuthenticatedUser,
) -> ReviewRead:
    review = await review_service.add_new_from_user(schema, user.id, studio.id)
    return review


@router.put(
    "/studios/{studio_id}/reviews/{review_id}", response_model=ReviewRead
)
async def update_my_studio_review(
    review: OwnedReviewDep,
    schema: ReviewUpdate,
    review_service: ReviewServiceDep,
    _: AuthenticatedUser,
) -> ReviewRead:
    return await review_service.update_by_id(review.id, schema)


@router.delete(
    "/studios/{studio_id}/reviews/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_my_studio_review(
    review: OwnedReviewDep,
    review_service: ReviewServiceDep,
    _: AuthenticatedUser,
) -> None:
    await review_service.delete_by_id(review.id)
