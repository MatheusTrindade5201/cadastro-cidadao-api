import pytest
from utils.helpers.residence_helpers.validate_city_by_uf import validate_city_by_uf
from utils.exceptions.exception import InvalidCityForState

@pytest.mark.asyncio
async def test_validate_city_by_uf_found(monkeypatch):
    async def mock_get_cities_by_uf(uf):
        if uf == 'SP':
            return [
                {"municipio-nome": "São Paulo"},
                {"municipio-nome": "Campinas"},
                {"municipio-nome": "Ribeirão Preto"}
            ]
        return []
    monkeypatch.setattr(
        'utils.helpers.residence_helpers.validate_city_by_uf.get_cities_by_uf',
        mock_get_cities_by_uf
    )
    result = await validate_city_by_uf('SP', 'São Paulo')
    assert result == 'São Paulo'
    result = await validate_city_by_uf('SP', 'campinas')
    assert result == 'Campinas'
    result = await validate_city_by_uf('SP', 'Ribeirao Preto')
    assert result == 'Ribeirão Preto'

@pytest.mark.asyncio
async def test_validate_city_by_uf_not_found(monkeypatch):
    async def mock_get_cities_by_uf(uf):
        if uf == 'SP':
            return [
                {"municipio-nome": "São Paulo"},
                {"municipio-nome": "Campinas"},
                {"municipio-nome": "Ribeirão Preto"}
            ]
        return []
    monkeypatch.setattr(
        'utils.helpers.residence_helpers.validate_city_by_uf.get_cities_by_uf',
        mock_get_cities_by_uf
    )
    with pytest.raises(InvalidCityForState):
        await validate_city_by_uf('SP', 'Sorocaba')
    with pytest.raises(InvalidCityForState):
        await validate_city_by_uf('RJ', 'Rio de Janeiro')
