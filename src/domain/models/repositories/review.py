from src.domain.models import Review
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.review import ReviewCreate, ReviewUpdate


class ReviewRepository(
    SQLAlchemyRepository[Review, ReviewCreate, ReviewUpdate]
):
    def __init__(self):
        super().__init__(Review)
