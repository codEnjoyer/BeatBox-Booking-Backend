from src.domain.models.review import Review
from src.domain.schemas.review import ReviewRead


def convert_model_to_scheme(review: Review) -> ReviewRead:
    return ReviewRead(
        id=review.id,
        author_id=review.author_id,
        studio_id=review.studio_id,
        grade=review.grade,
        text=review.text,
        date=review.date.isoformat(),
        room_id=review.room_id,
    )
