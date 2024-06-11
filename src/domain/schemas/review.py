from pydantic import Field

from src.domain.schemas.base import BaseSchema


class BaseReview(BaseSchema):
    grade: int = Field(..., gt=0, le=5)
    text: str


class ReviewRead(BaseReview):
    id: int
    author_id: int
    date: str
    studio_id: int
    room_id: int | None


class ReviewCreate(BaseReview):
    room_id: int | None


class ReviewUpdate(BaseReview):
    ...
