from enum import Enum
from functools import wraps
from typing import Callable

from sqlalchemy.exc import IntegrityError

from config import Config

from persistency.connection import get_db
from utils.helpers.session_helpers.handle_integrity_error import handle_integrity_error


class QueryResponseOptions(str, Enum):
    All = "all"
    First = "first"

def get_database():
    return get_db


class ReadDatabaseSession:
    def __init__(
        self, query_type: QueryResponseOptions = QueryResponseOptions.All
    ):
        self.query_type = query_type

    def __call__(self, function):
        async def wrapper(*args, **kwargs):
            db = get_db
            async with await db() as session:
                # Call original function
                query = await function(*args, **kwargs)

                # Execute query
                result = await session.execute(query)

                if self.query_type == QueryResponseOptions.First:
                    return result.scalars().first()

                return result.scalars().all()

        return wrapper


class WriteDatabaseSession:
    def __init__(self, function):
        self.function = function
        wraps(function)(self)

    async def __call__(self, *args, **kwargs):
        db = get_db
        async with await db() as session:
            # Call original function
            query = await self.function(*args, **kwargs)

            result = await session.execute(query)

            await session.commit()

            return result


EXPECTED_INTEGRITY_ERRORS = ["user_login_per_day"]

class TransactionSession:
    def __call__(self, function: Callable):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            async with await get_database()() as session:
                try:
                    kwargs["session"] = session
                    result = await function(*args, **kwargs)
                    await session.commit()

                    return result

                except IntegrityError as e:
                    await session.rollback()
                    if any(
                        error in str(e) for error in EXPECTED_INTEGRITY_ERRORS
                    ):
                        pass
                    else:
                        print(f"Error during database operation: {e}")
                        handle_integrity_error(e)
                except Exception as e:
                    await session.rollback()
                    print(f"Error during database operation: {e}")
                    raise e

        return wrapper
