import pytest
from utils.helpers.validators.strong_password_validator import password_validator

# Senhas válidas
@pytest.mark.parametrize('pwd', [
    'Abcdef1!',
    'A1b2c3d4$',
    'SenhaForte9@',
    'XyZ123!@#',
    'Aaaaaa1@',
    'Abcdefghijklmnopq1!',  # 18 chars
    'A1b2c3d4e5f6g7h8i9J!', # 20 chars
])
def test_password_validator_valid(pwd):
    assert password_validator(pwd) is True

# Senhas inválidas
@pytest.mark.parametrize('pwd', [
    'abcdef1!',      # Sem maiúscula
    'ABCDEF1!',      # Sem minúscula
    'Abcdefgh!',     # Sem número
    'Abcdef12',      # Sem símbolo especial
    'Ab1!',          # Menos de 6 caracteres
    'Abcdefghijklmnopqrs1!@#$', # Mais de 20 caracteres
    '',              # Vazia
    None,            # None
])
def test_password_validator_invalid(pwd):
    assert password_validator(pwd if pwd is not None else '') is False

# Testa limites de tamanho
@pytest.mark.parametrize('pwd,expected', [
    ('A1b2c!', True),      # 6 caracteres
    ('A1b2c3d4e5f6g7h8i9J!', True), # 20 caracteres
    ('A1b2c', False),      # 5 caracteres
    ('A1b2c3d4e5f6g7h8i9J!@', False), # 21 caracteres
])
def test_password_validator_length_limits(pwd, expected):
    assert password_validator(pwd) is expected

# Testa símbolos especiais permitidos
@pytest.mark.parametrize('pwd', [
    'Abcdef1!',
    'Abcdef1@',
    'Abcdef1#',
    'Abcdef1$',
    'Abcdef1%',
    'Abcdef1^',
    'Abcdef1&',
    'Abcdef1*',
    'Abcdef1(',
    'Abcdef1[',
    'Abcdef1]',
    'Abcdef1-',
    'Abcdef1_',
    'Abcdef1=',
    'Abcdef1+',
])
def test_password_validator_special_symbols(pwd):
    assert password_validator(pwd) is True

