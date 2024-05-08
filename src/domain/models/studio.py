from sqlalchemy import String, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.domain.models.base import BaseModel


class Studio(BaseModel):
    __tablename__ = "studios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500))

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="studio", lazy="joined", cascade="all, delete-orphan"
    )
    rooms: Mapped[list["Room"]] = relationship(
        back_populates="studio", cascade="all, delete-orphan"
    )

    @hybrid_property
    def average_grade(self):
        return sum([review.grade for review in self.reviews]) / len(self.reviews)
