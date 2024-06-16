from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema, DatetimeTZ


class BaseReview(BaseSchema):
    grade: PositiveInt = Field(..., ge=1, le=5, examples=[4])
    text: str | None = Field(
        min_length=1, max_length=500, examples=["Nice", None]
    )
    room_id: PositiveInt | None = Field(examples=[1, None])


class ReviewRead(BaseReview):
    id: PositiveInt
    author: "UserRead"
    studio_id: PositiveInt
    published_at: DatetimeTZ


class ReviewCreate(BaseReview): ...


class ReviewUpdate(BaseReview): ...


from src.domain.schemas.user import UserRead

ReviewRead.update_forward_refs()
