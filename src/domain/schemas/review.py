from pydantic import Field, PositiveInt

from src.domain.schemas.base import BaseSchema, DatetimeTZ, IntID


class BaseReview(BaseSchema):
    grade: PositiveInt = Field(..., ge=1, le=5, examples=[4])
    text: str | None = Field(
        min_length=1, max_length=500, examples=["Nice", None]
    )
    room_id: IntID | None


class ReviewRead(BaseReview):
    id: IntID
    author: "UserRead"
    studio_id: IntID
    published_at: DatetimeTZ


class ReviewCreate(BaseReview): ...


class ReviewUpdate(BaseReview): ...


from src.domain.schemas.user import UserRead

ReviewRead.update_forward_refs()
