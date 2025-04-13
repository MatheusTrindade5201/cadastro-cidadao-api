from typing import Type

from sqlalchemy.orm import DeclarativeMeta



def validate_column_exists(model: Type[DeclarativeMeta], column: str) -> None:
    if not hasattr(model, column):
        raise ValueError(
            f"Column '{column}' does not exist in {model.__name__}"
        )