import re

from utils.exceptions.exception import InvalidZipCode
from utils.helpers.shared_helpers.remove_special_characters import remove_special_characters


def zip_code_validator(zip_code: str):
    pattern = r"^\d{5}-?\d{3}$"

    if not isinstance(zip_code, str) or not re.match(pattern, zip_code):
        raise InvalidZipCode(zip_code)

    return remove_special_characters(zip_code)