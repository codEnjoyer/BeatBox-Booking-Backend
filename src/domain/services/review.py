from sqlalchemy.exc import NoResultFound

from src.domain.models.review import Review
from src.domain.schemas.review import ReviewCreate, ReviewUpdate
from src.domain.exceptions.review import (
    ReviewNotFoundException,
    ReviewAlreadyExistException,
)
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
        if await self.is_review_from_user_exist(user_id, studio_id):
            raise ReviewAlreadyExistException()
        schema_dict = schema.model_dump()
        schema_dict["author_id"] = user_id
        schema_dict["studio_id"] = studio_id
        created = await self._repository.create(schema_dict)
        # NOTE: get_by_id is needed to load author
        return await self.get_by_id(created.id)

    async def is_review_from_user_exist(
        self, author_id: int, studio_id: int
    ) -> bool:
        try:
            await self._repository.get_one(
                self.model.studio_id == studio_id,
                self.model.author_id == author_id,
            )
        except NoResultFound:
            return False
        return True

    async def get_from_studio(
        self, studio_id: int, offset: int = 0, limit: int = 100
    ) -> list[Review]:
        return await self._repository.get_all(
            self.model.studio_id == studio_id, offset=offset, limit=limit
        )

    async def get_from_room(
        self, room_id: int, offset: int = 0, limit: int = 0
    ) -> list[Review]:
        return await self._repository.get_all(
            self.model.room_id == room_id, offset=offset, limit=limit
        )
