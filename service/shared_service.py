from typing import Any
from typing import List

from sqlalchemy import Column
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.helpers.service_helpers import validate_column_exists


class SharedService:
    @staticmethod
    async def select_model_fields(
        model,
        session: AsyncSession,
        field: str,
        value: Any,
        return_columns: List[Column],
        as_dict: bool = False,
    ):
        if not return_columns:
            raise ValueError(
                "At least one column must be specified for the return"
            )

        for col in return_columns:
            validate_column_exists(model, col.key)

        stmt = select(*return_columns).where(getattr(model, field) == value)
        result = await session.execute(stmt)
        row = result.first()

        if not row:
            return None

        if as_dict:
            return {col.key: val for col, val in zip(return_columns, row)}

        return row
