from src.domain.exceptions.studio import StudioNotFoundException
from src.domain.models import Studio
from src.domain.models.repositories.studio import StudioRepository
from src.domain.schemas.studio import StudioCreate, StudioUpdate
from src.domain.services.base import ModelService


class StudioService(ModelService[StudioRepository, Studio, StudioCreate, StudioUpdate]):
    def __init__(self):
        super().__init__(StudioRepository(), StudioNotFoundException)
