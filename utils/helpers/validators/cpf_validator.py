import re


def cpf_cleaner(cpf: str) -> str:
    # Gets CPF numbers and ignores other characters
    cpf_cleaned = "".join(re.findall(r"\d+", cpf))
    return cpf_cleaned


def cpf_validate(cpf: str) -> tuple:
    # Limpa todos os caracteres não numéricos
    cpf = cpf_cleaner(cpf)

    #  Checks if the CPF has 11 digits
    if len(cpf) != 11:
        return False, cpf

    #  Checks if the CPF has all the same numbers, eq: 11111111111
    if cpf == cpf[::-1]:
        return False, cpf

    #  Validates the two check digits
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        check = ((value * 10) % 11) % 10
        if check != int(cpf[i]):
            return False, cpf

    return True, cpf
