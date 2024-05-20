from datetime import datetime

from pydantic import Field

from src.domain.schemas.base import BaseSchema


class BaseReview(BaseSchema):
    grade: int = Field(ge=1, le=5)
    text: str


class ReviewRead(BaseReview):
    studio_id: int
    author_id: int
    date: datetime


class ReviewCreate(BaseReview):
    room_id: int


class ReviewUpdate(BaseReview):
    pass
