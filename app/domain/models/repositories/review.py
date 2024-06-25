from typing import override

from app.domain.models import Review
from app.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from app.domain.schemas.review import ReviewCreate, ReviewUpdate


class ReviewRepository(
    SQLAlchemyRepository[Review, ReviewCreate, ReviewUpdate]
):
    @override
    @property
    def model(self) -> type[Review]:
        return Review
