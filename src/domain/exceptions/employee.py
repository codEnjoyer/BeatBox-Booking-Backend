from src.domain.exceptions.base import ItemNotFoundException


class EmployeeNotFoundException(ItemNotFoundException):
    @property
    def item_name(self) -> str:
        return "Employee"
