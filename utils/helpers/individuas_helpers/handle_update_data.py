from persistency.schemas.individual_schemas import IndividualInput
from utils.exceptions.exception import InvalidEmail
from utils.helpers.individuas_helpers.validate_CPF import validate_CPF
from utils.helpers.validators.email_address_validator import email_validator


def handle_update_data(individual_input: IndividualInput):
    individual_data = individual_input.dict()
    update_data = {k: v for k, v in individual_data.items()
                   if k not in ["cuidadores", "condicoes", "deficiencias",
                                "doencas_cardiacas", "doencas_respiratorias",
                                "doencas_renais", "condicao_rua"]}

    if "cpf" in update_data:
        update_data["cpf"] = validate_CPF(update_data["cpf"])

    if "email" in update_data and update_data["email"]:
        if not email_validator(update_data["email"]):
            raise InvalidEmail(update_data["email"])

    return update_data
