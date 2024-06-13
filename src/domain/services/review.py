from fastapi import HTTPException
from starlette import status
from sqlalchemy.exc import NoResultFound

from src.domain.models.review import Review
from src.domain.schemas.review import ReviewCreate, ReviewUpdate
from src.domain.exceptions.review import ReviewNotFoundException
from src.domain.models.repositories.review import ReviewRepository
from src.domain.services.base import ModelService


class ReviewService(
    ModelService[ReviewRepository, Review, ReviewCreate, ReviewUpdate]
):
    def __init__(self):
        super().__init__(ReviewRepository(), ReviewNotFoundException)

    async def add_new_from_user(
        self, schema: ReviewCreate, user_id: int, studio_id: int
    ) -> Review:
        if await self.is_review_exist(user_id, studio_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has a review.py on this studio",
            )
        schema_dict = schema.model_dump()
        schema_dict.update(author_id=user_id, studio_id=studio_id)
        return await self._repository.create(schema_dict)

    async def is_review_exist(self, author_id: int, studio_id: int) -> bool:
        try:
            await self._repository.get_one(
                self.model.studio_id == studio_id,
                self.model.author_id == author_id,
            )
        except NoResultFound:
            return False
        return True

    async def get_studio_reviews(
        self, studio_id: int, offset: int = 0, limit: int = 100
    ) -> list[Review]:
        return await self._repository.get_all(
            self.model.studio_id == studio_id, offset=offset, limit=limit
        )
