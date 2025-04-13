from unidecode import unidecode

from utils.exceptions.exception import InvalidCityForState
from utils.helpers.residence_helpers.get_cities_by_uf import get_cities_by_uf


async def validate_city_by_uf(state_uf: str, city: str):
    state_cities = await get_cities_by_uf(state_uf)

    city_normalized = unidecode(city.lower())

    for state_city in state_cities:
        state_city_name_normalized = unidecode(
            state_city["municipio-nome"].lower()
        )

        if state_city_name_normalized == city_normalized:
            return state_city["municipio-nome"]

    raise InvalidCityForState(city, state_uf)
