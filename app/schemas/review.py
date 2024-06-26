from typing import Annotated

from pydantic import Field, PositiveInt

from schemas.base import (
    BaseSchema,
    DatetimeTZ,
    IntID,
    NonEmptyString,
)


class BaseReview(BaseSchema):
    grade: Annotated[PositiveInt, Field(..., ge=1, le=5, examples=[4])]
    text: (
        Annotated[NonEmptyString, Field(max_length=1024, examples=["Nice"])]
        | None
    )
    room_id: IntID | None


class ReviewRead(BaseReview):
    id: IntID
    author: "UserRead"
    studio_id: IntID
    published_at: DatetimeTZ


class ReviewCreate(BaseReview): ...


class ReviewUpdate(BaseReview): ...


from schemas.user import UserRead

ReviewRead.update_forward_refs()
