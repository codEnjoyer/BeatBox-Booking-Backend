from pydantic import BaseModel, constr


class UserAuthSchema(BaseModel):
    username: str
    hashed_password: constr(max_length=200)


class UserBaseSchema(BaseModel):
    username: str
    email: str


class UserCreateSchema(UserBaseSchema):
    hashed_password: constr(max_length=200)


class UserReadSchema(UserBaseSchema):
    id: int
    is_active: bool

    # reviews: list["Review"] = relationship(back_populates="author", cascade="all, delete-orphan")
    # reserved_slots: Mapped[list["Slot"]] = relationship(back_populates="booked_by")
