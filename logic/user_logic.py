from persistency.schemas.user_schemas import UserInput
from service.user_services import UserService
from utils.exceptions.exception import InvalidCpfInserted, InvalidEmailInserted, WeakPasswordInserted, UserAlreadyExists
from utils.helpers.validators.cpf_validator import cpf_validate
from utils.helpers.validators.email_address_validator import email_validator
from utils.helpers.validators.strong_password_validator import password_validator


class UserLogic:
    @staticmethod
    async def create_user_logic(user: UserInput) -> UserInput:
        is_valid_cpf, user.cpf = cpf_validate(user.cpf)

        if not is_valid_cpf:
            raise InvalidCpfInserted("Invalid CPF")

        is_valid_email = email_validator(user.email)

        if not is_valid_email:
            raise InvalidEmailInserted("Invalid email")

        is_strong_password = password_validator(user.password)

        if not is_strong_password:
            raise WeakPasswordInserted("Weak password")

        user_email_exists = await UserService.get_user(user.email)
        if user_email_exists:
            raise UserAlreadyExists("User already exists")

        await UserService.create_user(user)

        return user