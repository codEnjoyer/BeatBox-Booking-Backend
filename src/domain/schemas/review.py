import datetime

from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema


class BaseReview(BaseSchema):
    grade: PositiveInt = Field(..., gt=0, le=5)
    text: str | None
    room_id: PositiveInt | None


class ReviewRead(BaseReview):
    id: PositiveInt
    author: "UserRead"
    studio_id: PositiveInt
    published_at: datetime.datetime


class ReviewCreate(BaseReview): ...


class ReviewUpdate(BaseReview): ...


from src.domain.schemas.user import UserRead

ReviewRead.update_forward_refs()
