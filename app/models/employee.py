import typing

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if typing.TYPE_CHECKING:
    from models import User, Studio


class Employee(BaseModel):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    studio_id: Mapped[int] = mapped_column(
        ForeignKey("studios.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="employee", lazy="joined"
    )
    studio: Mapped["Studio"] = relationship(back_populates="employees")
