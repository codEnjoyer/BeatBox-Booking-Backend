import datetime

from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema


class BaseReview(BaseSchema):
    grade: PositiveInt = Field(..., gt=0, le=5)
    text: str | None
    room_id: PositiveInt | None


class ReviewRead(BaseReview):
    id: PositiveInt
    published_at: datetime.datetime
    author_id: PositiveInt
    studio_id: PositiveInt


class ReviewCreate(BaseReview):
    ...


class ReviewUpdate(BaseReview):
    ...
