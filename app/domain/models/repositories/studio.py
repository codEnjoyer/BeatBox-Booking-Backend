from typing import override

from app.domain.models import Studio
from app.domain.models.repositories.SQLAlchemy import SQLAlchemyRepository
from app.domain.schemas.studio import StudioCreate, StudioUpdate


class StudioRepository(
    SQLAlchemyRepository[Studio, StudioCreate, StudioUpdate]
):
    @override
    @property
    def model(self) -> type[Studio]:
        return Studio
