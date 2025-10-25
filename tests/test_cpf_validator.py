import pytest
from utils.helpers.validators.cpf_validator import cpf_validate

# CPFs válidos (com e sem formatação)
@pytest.mark.parametrize('cpf', [
    '123.456.789-09',
    '12345678909',
    '390.533.447-05',
    '39053344705',
])
def test_cpf_validate_valid(cpf):
    result, cleaned = cpf_validate(cpf)
    assert result is True
    assert len(cleaned) == 11
    assert cleaned.isdigit()

# CPFs inválidos (tamanho errado, todos iguais, caracteres não numéricos, dígitos errados)
@pytest.mark.parametrize('cpf', [
    '111.111.111-11',  # todos iguais
    '22222222222',     # todos iguais
    '123.456.789-00',  # dígitos errados
    '12345678900',     # dígitos errados
    '123.456.789',     # tamanho errado
    '123456789',       # tamanho errado
    'abc.def.ghi-jk',  # não numérico
    '',                # vazio
    None,              # None
])
def test_cpf_validate_invalid(cpf):
    result, cleaned = cpf_validate(cpf if cpf is not None else '')
    assert result is False
    assert len(cleaned) <= 11

# CPFs com caracteres especiais
@pytest.mark.parametrize('cpf', [
    '123.456.789-09',
    '123-456-789-09',
    '123 456 789 09',
    '123/456/789-09',
])
def test_cpf_validate_special_chars(cpf):
    result, cleaned = cpf_validate(cpf)
    assert len(cleaned) == 11
    assert cleaned.isdigit()

