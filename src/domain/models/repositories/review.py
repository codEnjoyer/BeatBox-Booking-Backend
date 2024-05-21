from sqlalchemy import ColumnElement, update

from src.domain.db import async_session_maker
from src.domain.models import Review
from src.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.review import ReviewCreate, ReviewUpdate


class ReviewRepository(
    SQLAlchemyRepository[Review, ReviewCreate, ReviewUpdate]
):
    def __init__(self):
        super().__init__(Review)

    async def update_one(
        self, schema: ReviewUpdate | dict[str, ...], *where: ColumnElement[bool]
    ) -> Review:
        schema = (
            schema.model_dump() if isinstance(schema, ReviewUpdate) else schema
        )
        async with async_session_maker() as session:
            stmt = (
                update(self._model)
                .where(*where)
                .values(**schema)
                .returning(self._model)
            )
            result = await session.execute(stmt)
            instances = result.scalar()
            await session.commit()
            return instances
