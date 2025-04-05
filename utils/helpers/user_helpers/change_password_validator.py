from persistency.models.models import User
from persistency.schemas.user_schemas import ChangePasswordInput
from utils.exceptions.exception import InvalidPasswordInserted, WeakPasswordInserted
from utils.providers.hash_provider import verify_hash
from utils.helpers.validators.strong_password_validator import password_validator


async def change_password_validator(
    passwords: ChangePasswordInput, user: User
):
    if not verify_hash(passwords.old_password, user.password):
        raise InvalidPasswordInserted(
            "The old password you provided is incorrect"
        )

    if not passwords.new_password == passwords.confirm_new_password:
        raise InvalidPasswordInserted(
            "The new password do not match, "
            "entry the same password in both fields"
        )

    if passwords.old_password == passwords.new_password:
        raise InvalidPasswordInserted(
            "The old and new passwords cannot be equals"
        )

    if not password_validator(passwords.new_password):
        raise WeakPasswordInserted("New password is not security")