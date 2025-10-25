import pytest
from utils.helpers.residence_helpers.validate_state_uf import validate_state_uf
from utils.exceptions.exception import InvalidStateUF

# Testa UFs válidos
@pytest.mark.parametrize('uf', ['SP', 'RJ', 'MG'])
def test_validate_state_uf_valid(monkeypatch, uf):
    monkeypatch.setattr('persistency.schemas.residence_schemas.STATES_MAP', {'SP': 'São Paulo', 'RJ': 'Rio de Janeiro', 'MG': 'Minas Gerais'})
    # Não deve levantar exceção
    validate_state_uf(uf)

# Testa UF inválido
@pytest.mark.parametrize('uf', ['XX', '', None])
def test_validate_state_uf_invalid(monkeypatch, uf):
    monkeypatch.setattr('persistency.schemas.residence_schemas.STATES_MAP', {'SP': 'São Paulo', 'RJ': 'Rio de Janeiro', 'MG': 'Minas Gerais'})
    with pytest.raises(InvalidStateUF):
        validate_state_uf(uf)

