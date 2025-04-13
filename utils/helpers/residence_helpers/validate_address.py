from persistency.schemas.residence_schemas import ResidenceInput
from utils.helpers.residence_helpers.validate_city_by_uf import validate_city_by_uf
from utils.helpers.residence_helpers.validate_state_uf import validate_state_uf
from utils.helpers.residence_helpers.zip_code_validator import zip_code_validator


async def validate_delivery_address_creation(
    residence_input: ResidenceInput,
):
    validate_state_uf(residence_input.uf)

    residence_input.municipio = await validate_city_by_uf(
        residence_input.uf, residence_input.municipio
    )

    residence_input.cep = zip_code_validator(
        residence_input.cep
    )

    return residence_input
