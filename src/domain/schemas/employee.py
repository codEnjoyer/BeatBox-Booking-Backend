from pydantic import Field

from src.domain.schemas.base import BaseSchema, IntID


class BaseEmployee(BaseSchema):
    name: str = Field(min_length=3)


class EmployeeRead(BaseEmployee):
    id: IntID
    studio_id: IntID
    user_id: IntID


class EmployeeCreate(BaseEmployee):
    user_id: IntID


class EmployeeUpdate(BaseEmployee): ...
