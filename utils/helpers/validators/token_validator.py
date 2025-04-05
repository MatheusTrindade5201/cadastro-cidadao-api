from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from service.user_services import UserService
from persistency.schemas.user_schemas import RoleOptions
from utils.exceptions.exception import ForbiddenToken, UnauthorizedLogin, UnauthorizedAccess
from utils.providers.token_provider import verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def validate_session(token: str = Depends(oauth2_scheme)):
    payload = verify_jwt_token(token)
    return payload


async def validate_session_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = validate_session(token)
        user = await UserService.get_user(payload["sub"])
        if not user or user.role != RoleOptions.Admin:
            raise ForbiddenToken("Not authorized")

        return payload
    except Exception as err:
        raise UnauthorizedLogin(err.detail)


def validate_session_with_roles(*valid_roles: RoleOptions):
    async def _validate_session(token: str = Depends(oauth2_scheme)):
        try:
            payload = validate_session(token)
            user = await UserService.get_user(payload["sub"])

            if user.role  not in valid_roles:
                raise ForbiddenToken("Not authorized")

            return payload
        except Exception as err:
            raise UnauthorizedAccess(err.detail)

    return _validate_session
