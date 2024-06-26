from typing import override

from models import Review
from models.repositories.SQLAlchemy import SQLAlchemyRepository
from schemas.review import ReviewCreate, ReviewUpdate


class ReviewRepository(
    SQLAlchemyRepository[Review, ReviewCreate, ReviewUpdate]
):
    @override
    @property
    def model(self) -> type[Review]:
        return Review
