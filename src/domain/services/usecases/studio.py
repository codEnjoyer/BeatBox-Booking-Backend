from src.domain.exceptions.studio import StudioNotFoundException
from src.domain.models.base import BaseModel
from src.domain.models.repositories.studio import StudioRepository
from src.domain.schemas.studio import StudioCreate
from src.domain.services.usecases.common import CreateUseCase, GetByIdUseCase, UpdateByIdUseCase, \
    DeleteByIdUseCase
from src.domain.services.usecases.common.get_all import GetAllUseCase

from src.models import Studio


class CreateStudioUseCase(CreateUseCase[Studio, StudioCreate, StudioRepository]):
    _model: BaseModel = Studio


class GetAllStudiosUseCase(GetAllUseCase[Studio, StudioRepository]):
    _model: BaseModel = Studio


class GetStudioByIdUseCase(GetByIdUseCase[int, Studio, StudioRepository]):
    _model: BaseModel = Studio
    _not_found_exception: Exception = StudioNotFoundException


class GetStudioByNameUseCase(GetByIdUseCase[str, Studio, StudioRepository]):
    _model: BaseModel = Studio
    _not_found_exception: Exception = StudioNotFoundException


class UpdateStudioByIdUseCase(UpdateByIdUseCase[int, Studio, StudioCreate, StudioRepository]):
    _model: BaseModel = Studio


class DeleteStudioByIdUseCase(DeleteByIdUseCase[int, Studio, StudioRepository]):
    _model: BaseModel = Studio
    _not_found_exception: Exception = StudioNotFoundException
