from datetime import datetime, timezone

from fastapi import HTTPException
from starlette import status
from sqlalchemy.exc import NoResultFound

from src.domain.models.review import Review
from src.domain.schemas.review import ReviewCreate, ReviewUpdate, ReviewRead
from src.domain.exceptions.review import ReviewNotFoundException
from src.domain.models.repositories.review import ReviewRepository
from src.domain.services.base import ModelService


class ReviewService(
    ModelService[ReviewRepository, Review, ReviewCreate, ReviewUpdate]
):
    def __init__(self):
        super().__init__(ReviewRepository(), ReviewNotFoundException)

    async def create(self, schema: ReviewCreate, **kwargs) -> ReviewRead:
        author_id: int = kwargs.get('author_id')
        studio_id: int = kwargs.get('studio_id')
        if not self.is_review_already_exist(author_id, studio_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has a review on this studio",
            )
        review_data = schema.model_dump()
        review_data["author_id"] = author_id
        review_data["studio_id"] = studio_id

        review = await self._repository.create(review_data)
        return ReviewRead.model_validate(review)

    async def is_review_already_exist(
        self, author_id: int, studio_id: int
    ) -> bool:
        try:
            await self._repository.get_one(
                self._model.studio_id == studio_id,
                self._model.author_id == author_id,
            )
        except NoResultFound:
            return False
        return True

    async def get_reviews_by_studio_id(
        self, studio_id: int, offset: int = 0, limit: int = 100
    ) -> list[Review]:
        return await self._repository.get_all(
            self._model.studio_id == studio_id, offset=offset, limit=limit
        )

    async def patch_review(
        self,
        studio_id: int,
        author_id: int,
        review_id: int,
        schema: ReviewUpdate,
    ) -> Review:
        if not self.is_review_already_exist(
            studio_id=studio_id, author_id=author_id
        ):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="User does not have review on this studio",
            )
        scalar = await self._repository.update(schema, self._model.id == review_id)
        return scalar
