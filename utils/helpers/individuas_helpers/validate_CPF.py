from utils.exceptions.exception import InvalidCPF
from utils.helpers.validators.cpf_validator import cpf_validate


def validate_CPF(cpf: str):
    is_valid, cpf = cpf_validate(cpf)

    if not is_valid:
        raise InvalidCPF(cpf)

    return cpf
