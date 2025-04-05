import re


def password_validator(password: str) -> bool:
    # Must have at least one number.
    # Must have at least one uppercase and one lowercase character.
    # Must have at least one special symbol.
    # Must be between 6 and 20 characters long.
    regex = (
        r"^(?=.*[A-Z])(?=.*[!@#$%^&*(\[\])\-_=+])"
        r"(?=.*[0-9])(?=.*[a-z]).{6,20}$"
    )
    if not re.match(regex, password):
        return False

    return True
