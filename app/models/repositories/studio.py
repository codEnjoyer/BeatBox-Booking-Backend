from typing import override

from models import Studio
from models.repositories.SQLAlchemy import SQLAlchemyRepository
from schemas.studio import StudioCreate, StudioUpdate


class StudioRepository(
    SQLAlchemyRepository[Studio, StudioCreate, StudioUpdate]
):
    @override
    @property
    def model(self) -> type[Studio]:
        return Studio
