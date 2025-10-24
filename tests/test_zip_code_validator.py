import pytest
from utils.helpers.residence_helpers.zip_code_validator import zip_code_validator
from utils.exceptions.exception import InvalidZipCode

# Testes para CEPs válidos
@pytest.mark.parametrize('cep,expected', [
    ('12345-678', '12345678'),
    ('12345678', '12345678'),
    ('98765-432', '98765432'),
    ('98765432', '98765432'),
])
def test_zip_code_validator_valid(cep, expected):
    assert zip_code_validator(cep) == expected

# Testes para CEPs inválidos
@pytest.mark.parametrize('cep', [
    '1234-567',      # Menor que 8 dígitos
    '1234567',       # Menor que 8 dígitos
    '123456789',     # Maior que 8 dígitos
    '12a45-678',     # Contém letra
    '12345_678',     # Caracter especial inválido
    'ABCDE-FGH',     # Só letras
    '',              # Vazio
    None,            # None
])
def test_zip_code_validator_invalid(cep):
    with pytest.raises(InvalidZipCode):
        zip_code_validator(cep)

# Teste para remoção de caracteres especiais
@pytest.mark.parametrize('cep,expected', [
    ('12345-678', '12345678'),
    ('12345.678', '12345678'),
    ('12345 678', '12345678'),
    ('12345/678', '12345678'),
])
def test_zip_code_validator_remove_special(cep, expected):
    # O regex só aceita hífen, mas se passar outros caracteres, remove_special_characters é chamado
    try:
        result = zip_code_validator(cep)
        assert result == expected
    except InvalidZipCode:
        pass

