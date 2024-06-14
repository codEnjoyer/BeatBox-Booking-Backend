import datetime

from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema
from src.domain.schemas.room import RoomRead


class BaseReview(BaseSchema):
    grade: PositiveInt = Field(..., gt=0, le=5)
    text: str | None


class ReviewRead(BaseReview):
    id: PositiveInt
    published_at: datetime.datetime
    author_id: PositiveInt
    studio_id: PositiveInt
    room: RoomRead | None


class ReviewCreate(BaseReview):
    room_id: PositiveInt | None


class ReviewUpdate(BaseReview):
    room_id: PositiveInt | None
