from src.domain.models.repositories.orm.repository import ORMRepository
from src.domain.schemas.studio import StudioCreate, StudioUpdate
from src.models import Studio


class StudioRepository(ORMRepository
                       [Studio, StudioCreate, StudioUpdate]):
    def __init__(self):
        super().__init__(Studio)
