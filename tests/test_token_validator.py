import pytest
import pytest_asyncio
from utils.helpers.validators.token_validator import validate_session_with_roles
from utils.exceptions.exception import ForbiddenToken, UnauthorizedAccess, UnauthorizedLogin

class MockUser:
    def __init__(self, role):
        self.role = role

@pytest_asyncio.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    # Mock validate_session para sempre retornar um payload
    monkeypatch.setattr('utils.helpers.validators.token_validator.validate_session', lambda token: {'sub': 'user_id'})
    # Mock UserService.get_user para retornar usuário com role
    class UserService:
        @staticmethod
        async def get_user(sub):
            return MockUser(role='admin')
    monkeypatch.setattr('utils.helpers.validators.token_validator.UserService', UserService)

@pytest.mark.asyncio
async def test_validate_session_with_roles_success():
    validator = validate_session_with_roles('admin', 'user')
    payload = await validator(token='valid_token')
    assert payload['sub'] == 'user_id'

@pytest.mark.asyncio
async def test_validate_session_with_roles_forbidden(monkeypatch):
    # Mock UserService.get_user para retornar role não permitido
    class UserService:
        @staticmethod
        async def get_user(sub):
            return MockUser(role='guest')
    monkeypatch.setattr('utils.helpers.validators.token_validator.UserService', UserService)
    validator = validate_session_with_roles('admin', 'user')
    with pytest.raises(UnauthorizedAccess):
        await validator(token='valid_token')

@pytest.mark.asyncio
async def test_validate_session_with_roles_invalid_token(monkeypatch):
    # Mock validate_session para levantar UnauthorizedLogin
    def raise_invalid(token):
        raise UnauthorizedLogin('Token inválido')
    monkeypatch.setattr('utils.helpers.validators.token_validator.validate_session', raise_invalid)
    validator = validate_session_with_roles('admin')
    with pytest.raises(UnauthorizedAccess):
        await validator(token='invalid_token')

