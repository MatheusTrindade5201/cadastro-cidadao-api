from sqlalchemy.exc import IntegrityError

from utils.exceptions.exception import EntityNotExists


def handle_integrity_error(error: IntegrityError):
    """
    Handles database integrity errors by raising mapped custom exceptions.

    Purpose:
    Maps foreign key and unique constraint violations to specific exceptions
    for meaningful error responses.

    Organization:
    - `foreign_key_exceptions`: Maps foreign key constraint keys (e.g., "segment_id") to exceptions.
    - `unique_constraint_exceptions`: Maps unique constraint keys (e.g., "pedagogical_journeys_name_key") to exceptions.

    To Add a New Error:
    1. Identify the constraint key from the error message.
    2. Add the key and corresponding exception to the appropriate mapping.
    """
    error_message = str(error.orig)

    if "foreign key constraint" in error_message:
        for key, exception in foreign_key_exceptions.items():
            if key in error_message:
                raise exception

    elif "duplicate key value violates unique constraint" in error_message:
        for key, exception in unique_constraint_exceptions.items():
            if key in error_message:
                raise exception()

    raise error

def entity_not_exists_message(entity_name: str) -> EntityNotExists:
    return EntityNotExists(f"The provided {entity_name} does not exist.")


foreign_key_exceptions = {}

unique_constraint_exceptions = {}

