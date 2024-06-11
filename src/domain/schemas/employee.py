from src.domain.schemas.base import BaseSchema


class BaseEmployee(BaseSchema):
    studio_id: int


class EmployeeRead(BaseEmployee):
    id: int
    user_id: int


class EmployeeCreate(BaseEmployee):
    user_id: int


class EmployeeUpdate(BaseEmployee):
    ...
