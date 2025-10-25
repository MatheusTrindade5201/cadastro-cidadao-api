import pytest
from utils.helpers.individuas_helpers.format_individual_residences import format_individual_residences
from utils.helpers.individuas_helpers.handle_update_data import handle_update_data
from utils.helpers.individuas_helpers.validate_CPF import validate_CPF
from utils.exceptions.exception import InvalidCPF, InvalidEmail

# Mock para format_individual_residences
def test_format_individual_residences_basic():
    class DomicilioIndividuo:
        domicilio_id = 1
        data_residencia = None
        mudou = True
        renda_familia_salario_minimos = '2.0'
        n_membros_familia = 4
        responsavel = 'João'
    class Residencia:
        pass
    residencia = Residencia()
    residencia.DomicilioIndividuo = DomicilioIndividuo()
    residencia.tipo_logradouro = 'Rua'
    residencia.nome_logradouro = 'A'
    residencia.numero = '123'
    residencia.complemento = None
    residencia.bairro = 'Centro'
    residencia.municipio = 'Cidade'
    residencia.uf = 'SP'
    residencia.cep = '12345-678'
    result = format_individual_residences([residencia])
    assert result[0]['domicilio_id'] == 1
    assert result[0]['endereco_completo'] == 'Rua A, 123'

# Teste para handle_update_data
class MockInput:
    def __init__(self, cpf, email):
        self.cuidadores = None
        self.condicoes = None
        self.deficiencias = None
        self.doencas_cardiacas = None
        self.doencas_respiratorias = None
        self.doencas_renais = None
        self.condicao_rua = None
        self.cpf = cpf
        self.email = email
    def dict(self):
        return self.__dict__

def test_handle_update_data_valid():
    input_data = MockInput('12345678909', 'email@email.com')
    # email_validator sempre retorna True, cpf_validate retorna True, cpf
    from utils.helpers.validators.email_address_validator import email_validator
    from utils.helpers.validators.cpf_validator import cpf_validate
    # monkeypatch para garantir validação
    assert handle_update_data(input_data)['cpf'] == '12345678909'

def test_handle_update_data_invalid_email(monkeypatch):
    input_data = MockInput('12345678909', 'email_invalido')
    monkeypatch.setattr('utils.helpers.validators.email_address_validator.email_validator', lambda x: False)
    with pytest.raises(InvalidEmail):
        handle_update_data(input_data)

def test_validate_CPF_valid(monkeypatch):
    monkeypatch.setattr('utils.helpers.validators.cpf_validator.cpf_validate', lambda cpf: (True, cpf))
    assert validate_CPF('12345678909') == '12345678909'

def test_validate_CPF_invalid(monkeypatch):
    monkeypatch.setattr('utils.helpers.validators.cpf_validator.cpf_validate', lambda cpf: (False, cpf))
    with pytest.raises(InvalidCPF):
        validate_CPF('00000000000')

# Para funções assíncronas, recomenda-se usar pytest-asyncio e mocks
# Testes para funções assíncronas podem ser adicionados conforme necessário
