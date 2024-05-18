from src.domain.schemas.base import BaseSchema


class BaseReview(BaseSchema):
    grade: int
    text: str


class ReviewRead(BaseReview):
    author_id: int
    date: str


class ReviewCreate(BaseReview):
    studio_id: int
    room_id: int


class ReviewUpdate(BaseReview):
    pass
