from persistency.models.models import Domicilio
from persistency.schemas.residence_schemas import ResidenceInputPatch
from utils.helpers.residence_helpers.validate_city_by_uf import validate_city_by_uf
from utils.helpers.residence_helpers.validate_state_uf import validate_state_uf
from utils.helpers.residence_helpers.zip_code_validator import zip_code_validator


async def validate_residence_update(
    residence_input: ResidenceInputPatch, residence: Domicilio
):
    if residence_input.uf:
        validate_state_uf(residence_input.uf.upper())

    if residence_input.municipio or residence_input.uf:
        uf = residence_input.uf or residence.uf
        municipio = residence_input.municipio or residence.municipio
        residence_input.municipio = await validate_city_by_uf(
            uf, municipio
        )

    if residence_input.cep:
        residence_input.cep = zip_code_validator(
            residence_input.cep
        )
