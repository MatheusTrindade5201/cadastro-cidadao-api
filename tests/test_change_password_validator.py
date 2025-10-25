import pytest
from utils.helpers.user_helpers.change_password_validator import change_password_validator
from utils.exceptions.exception import InvalidPasswordInserted, WeakPasswordInserted

class MockUser:
    def __init__(self, password):
        self.password = password

class MockChangePasswordInput:
    def __init__(self, old_password, new_password, confirm_new_password):
        self.old_password = old_password
        self.new_password = new_password
        self.confirm_new_password = confirm_new_password

@pytest.mark.asyncio
async def test_change_password_success(monkeypatch):
    user = MockUser(password='hashed_old')
    input_data = MockChangePasswordInput('old', 'newStrong1!', 'newStrong1!')
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.verify_hash', lambda raw, hashed: raw == 'old' and hashed == 'hashed_old')
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.password_validator', lambda pwd: True)
    await change_password_validator(input_data, user)

@pytest.mark.asyncio
async def test_change_password_wrong_old(monkeypatch):
    user = MockUser(password='hashed_old')
    input_data = MockChangePasswordInput('wrong', 'newStrong1!', 'newStrong1!')
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.verify_hash', lambda raw, hashed: False)
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.password_validator', lambda pwd: True)
    with pytest.raises(InvalidPasswordInserted):
        await change_password_validator(input_data, user)

@pytest.mark.asyncio
async def test_change_password_mismatch(monkeypatch):
    user = MockUser(password='hashed_old')
    input_data = MockChangePasswordInput('old', 'newStrong1!', 'different')
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.verify_hash', lambda raw, hashed: True)
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.password_validator', lambda pwd: True)
    with pytest.raises(InvalidPasswordInserted):
        await change_password_validator(input_data, user)

@pytest.mark.asyncio
async def test_change_password_same_as_old(monkeypatch):
    user = MockUser(password='hashed_old')
    input_data = MockChangePasswordInput('old', 'old', 'old')
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.verify_hash', lambda raw, hashed: True)
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.password_validator', lambda pwd: True)
    with pytest.raises(InvalidPasswordInserted):
        await change_password_validator(input_data, user)

@pytest.mark.asyncio
async def test_change_password_weak(monkeypatch):
    user = MockUser(password='hashed_old')
    input_data = MockChangePasswordInput('old', 'weak', 'weak')
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.verify_hash', lambda raw, hashed: True)
    monkeypatch.setattr('utils.helpers.user_helpers.change_password_validator.password_validator', lambda pwd: False)
    with pytest.raises(WeakPasswordInserted):
        await change_password_validator(input_data, user)

