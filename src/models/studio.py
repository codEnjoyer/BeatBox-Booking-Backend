from sqlalchemy import Integer, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.db import Base


class Studio(Base):
    __tablename__ = "studios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500))
    reviews: Mapped[list["Review"]] = relationship(back_populates="studio", lazy="joined")
    slots: Mapped[list["Slot"]] = relationship(back_populates="studio")

    @hybrid_property
    def average_grade(self):
        return sum([review.grade for review in self.reviews]) / len(self.reviews)
