from fastapi import APIRouter, HTTPException
from starlette import status

from src.api.v1.dependencies.review import OwnedReviewDep
from src.api.v1.dependencies.room import ValidStudioRoomNameDep
from src.api.v1.dependencies.services import ReviewServiceDep, RoomServiceDep
from src.api.v1.dependencies.auth import AuthenticatedUser
from src.api.v1.dependencies.studio import ValidStudioIdDep
from src.api.v1.dependencies.types import QueryOffset, QueryLimit
from src.domain.exceptions.review import ReviewAlreadyExistException
from src.domain.exceptions.room import (
    RoomNotFoundException,
    RoomDoesNotExistInStudioException,
)
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


@router.post("/studios/{studio_id}/reviews",
             response_model=ReviewRead)
async def post_review_on_studio(
    studio: ValidStudioIdDep,
    schema: ReviewCreate,
    review_service: ReviewServiceDep,
    room_service: RoomServiceDep,
    user: AuthenticatedUser,
) -> ReviewRead:
    if schema.room_id:
        try:
            await room_service.check_if_room_in_studio(
                schema.room_id, studio.id
            )
        except RoomNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            ) from e
        except RoomDoesNotExistInStudioException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            ) from e
    # TODO: add check if user has bookings in this studio (and room)
    try:
        review = await review_service.add_new_from_user(
            schema, user.id, studio.id
        )
    except ReviewAlreadyExistException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e
    return review


@router.put(
    "/studios/{studio_id}/reviews/{review_id}", response_model=ReviewRead
)
async def update_my_studio_review(
    review: OwnedReviewDep,
    schema: ReviewUpdate,
    review_service: ReviewServiceDep,
    room_service: RoomServiceDep,
    _: AuthenticatedUser,
) -> ReviewRead:
    if schema.room_id:
        try:
            await room_service.check_if_room_in_studio(
                schema.room_id, review.studio_id
            )
        except RoomNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            ) from e
        except RoomDoesNotExistInStudioException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            ) from e
    updated = await review_service.update_by_id(review.id, schema)
    with_author = await review_service.get_by_id(updated.id)
    return with_author


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
