from src.domain.models.repositories.studio import StudioRepository
from src.domain.services.usecases.studio import DeleteStudioByIdUseCase, CreateStudioUseCase, \
    UpdateStudioByIdUseCase, GetStudioByIdUseCase, GetStudioByNameUseCase, GetAllStudiosUseCase
from src.domain.models import Studio


class StudioService(CreateStudioUseCase,
                    GetStudioByIdUseCase,
                    GetStudioByNameUseCase,
                    GetAllStudiosUseCase,
                    UpdateStudioByIdUseCase,
                    DeleteStudioByIdUseCase):
    def __init__(self):
        super().__init__(Studio, StudioRepository)
