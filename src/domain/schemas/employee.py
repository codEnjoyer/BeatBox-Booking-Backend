from src.domain.schemas.base import BaseSchema, IntID, NonEmptyString


class BaseEmployee(BaseSchema):
    name: NonEmptyString


class EmployeeRead(BaseEmployee):
    id: IntID
    studio_id: IntID
    user_id: IntID


class EmployeeCreate(BaseEmployee):
    user_id: IntID


class EmployeeUpdate(BaseEmployee): ...
