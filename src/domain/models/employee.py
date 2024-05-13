import typing

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import BaseModel

if typing.TYPE_CHECKING:
    from src.domain.models.user import User
    from src.domain.models.studio import Studio


class Employee(BaseModel):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    studio_id: Mapped[int] = mapped_column(ForeignKey("studios.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="employee")
    studio: Mapped["Studio"] = relationship(back_populates="employees")
