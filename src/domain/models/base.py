from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class BaseModel(Base):
    __abstract__ = True

    _repr_cols_num = 3
    _repr_cols = tuple()

    def update(self, **new_fields: dict[str, ...]) -> None:
        for attr, value in new_fields.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        columns = []
        for index, column in enumerate(self.__table__.columns.keys()):
            if column in self._repr_cols or index < self._repr_cols_num:
                columns.append(f"{column}={getattr(self, column)}")

        return f"<{self.__class__.__name__} {', '.join(columns)}>"
