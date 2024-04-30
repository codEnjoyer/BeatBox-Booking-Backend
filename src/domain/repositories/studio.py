from src.domain.repositories.SQLAlchemy import SQLAlchemyRepository
from src.domain.schemas.studio import StudioCreate, StudioUpdate
from src.models import Studio


class StudioRepository(SQLAlchemyRepository
                       [Studio, StudioCreate, StudioUpdate]):
    def __init__(self):
        super().__init__(Studio)
