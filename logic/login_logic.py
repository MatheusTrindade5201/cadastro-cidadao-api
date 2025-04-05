from persistency.schemas.login_schemas import LoginInput, LoginOutput
from service.user_services import UserService
from utils.exceptions.exception import UnauthorizedLogin
from utils.providers.hash_provider import verify_hash
from utils.providers.token_provider import jwt_encoder
from utils.helpers.validators.cpf_validator import cpf_cleaner
from utils.helpers.validators.email_address_validator import email_validator


class LoginLogic:
    @staticmethod
    async def user_login_logic(login_data: LoginInput) -> LoginOutput:
        if not email_validator(login_data.username):
            login_data.username = cpf_cleaner(login_data.username)

        user = await UserService.get_user(login_data.username)

        if not user or not verify_hash(login_data.password, user.password):
            raise UnauthorizedLogin("Authenticate failed")

        token = jwt_encoder({"sub": login_data.username})

        return LoginOutput(access_token = token)
