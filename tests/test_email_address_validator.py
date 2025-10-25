import pytest
from utils.helpers.validators.email_address_validator import email_validator

# E-mails válidos
@pytest.mark.parametrize('email', [
    'teste@email.com',
    'user.name+tag@sub.domain.com',
    'usuario@dominio.com.br',
    'user_name@domain.co',
    'user-name@domain.info',
    'user@exemplo.museum',
    'usário_unicode@domínio.com',
])
def test_email_validator_valid(email):
    assert email_validator(email) is True

# E-mails inválidos
@pytest.mark.parametrize('email', [
    'plainaddress',
    '@missingusername.com',
    'username@',
    'username@.com',
    'username@com',
    'username@domain..com',
    'username@domain,com',
    'username@domain com',
    'username@domain#com',
    'username@domain@com',
    'username@.domain.com',
    'username@domain..com',
    'user name@domain.com',
    '',
    None,
])
def test_email_validator_invalid(email):
    assert email_validator(email if email is not None else '') is False

