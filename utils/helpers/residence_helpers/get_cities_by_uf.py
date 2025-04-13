import aiohttp

from utils.exceptions.exception import ExternalServiceFailure


async def get_cities_by_uf(uf: str):
    URL = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios?view=nivelado"

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            dict_response = await response.json()

            if response.status == 200:
                return dict_response

            raise ExternalServiceFailure()
