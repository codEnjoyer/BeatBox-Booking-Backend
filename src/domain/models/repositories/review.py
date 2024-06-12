from typing import override

from src.domain.models import Review
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.review import ReviewCreate, ReviewUpdate


class ReviewRepository(
    SQLAlchemyRepository[Review, ReviewCreate, ReviewUpdate]
):
    @override
    @property
    def model(self) -> type[Review]:
        return Review
