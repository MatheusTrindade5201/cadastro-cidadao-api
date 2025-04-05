from email_validator import EmailNotValidError, validate_email


def email_validator(email: str) -> bool:
    try:
        # Check that the email address is valid.
        validate_email(email)

        # Take the normalized form of the email address
        # for all logic beyond this point (especially
        # before going to a database query where equality
        # may not take into account Unicode normalization).
        return True

    except EmailNotValidError:
        # Email is not valid.
        # The exception message is human-readable.
        return False
