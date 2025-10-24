import pytest
import pytest_asyncio
from utils.helpers.residence_helpers.validate_residence_update import validate_residence_update

class MockResidenceInput:
    def __init__(self, uf=None, municipio=None, cep=None):
        self.uf = uf
        self.municipio = municipio
        self.cep = cep

class MockResidence:
    def __init__(self, uf='SP', municipio='São Paulo', cep='01000-000'):
        self.uf = uf
        self.municipio = municipio
        self.cep = cep

@pytest.mark.asyncio
async def test_update_with_all_fields(monkeypatch):
    input_data = MockResidenceInput(uf='RJ', municipio='Niterói', cep='24000-000')
    residence = MockResidence()
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_state_uf', lambda uf: uf)
    async def mock_validate_city_by_uf(uf, mun):
        return mun.title()
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_city_by_uf', mock_validate_city_by_uf)
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.zip_code_validator', lambda cep: f'VALID-{cep}')
    await validate_residence_update(input_data, residence)
    assert input_data.uf == 'RJ'
    assert input_data.municipio == 'Niterói'
    assert input_data.cep == 'VALID-24000-000'

@pytest.mark.asyncio
async def test_update_only_uf(monkeypatch):
    input_data = MockResidenceInput(uf='MG')
    residence = MockResidence(uf='SP', municipio='Campinas')
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_state_uf', lambda uf: uf)
    async def mock_validate_city_by_uf(uf, mun):
        return mun.title()
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_city_by_uf', mock_validate_city_by_uf)
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.zip_code_validator', lambda cep: cep)
    await validate_residence_update(input_data, residence)
    assert input_data.uf == 'MG'
    assert input_data.municipio == 'Campinas'

@pytest.mark.asyncio
async def test_update_only_municipio(monkeypatch):
    input_data = MockResidenceInput(municipio='Ribeirão Preto')
    residence = MockResidence(uf='SP', municipio='Campinas')
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_state_uf', lambda uf: uf)
    async def mock_validate_city_by_uf(uf, mun):
        return mun.title()
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_city_by_uf', mock_validate_city_by_uf)
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.zip_code_validator', lambda cep: cep)
    await validate_residence_update(input_data, residence)
    assert input_data.uf is None
    assert input_data.municipio == 'Ribeirão Preto'

@pytest.mark.asyncio
async def test_update_only_cep(monkeypatch):
    input_data = MockResidenceInput(cep='12345-678')
    residence = MockResidence()
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_state_uf', lambda uf: uf)
    async def mock_validate_city_by_uf(uf, mun):
        return mun
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_city_by_uf', mock_validate_city_by_uf)
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.zip_code_validator', lambda cep: f'VALID-{cep}')
    await validate_residence_update(input_data, residence)
    assert input_data.cep == 'VALID-12345-678'

@pytest.mark.asyncio
async def test_update_invalid_uf(monkeypatch):
    input_data = MockResidenceInput(uf='XX')
    residence = MockResidence()
    def raise_invalid_uf(uf):
        raise ValueError('UF inválido')
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_state_uf', raise_invalid_uf)
    async def mock_validate_city_by_uf(uf, mun):
        return mun
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_city_by_uf', mock_validate_city_by_uf)
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.zip_code_validator', lambda cep: cep)
    with pytest.raises(ValueError):
        await validate_residence_update(input_data, residence)

@pytest.mark.asyncio
async def test_update_invalid_municipio(monkeypatch):
    input_data = MockResidenceInput(municipio='CidadeInexistente')
    residence = MockResidence(uf='SP', municipio='Campinas')
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_state_uf', lambda uf: uf)
    async def raise_invalid_city(uf, mun):
        raise ValueError('Município inválido')
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.validate_city_by_uf', raise_invalid_city)
    monkeypatch.setattr('utils.helpers.residence_helpers.validate_residence_update.zip_code_validator', lambda cep: cep)
    with pytest.raises(ValueError):
        await validate_residence_update(input_data, residence)
