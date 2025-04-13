from wsgiref.validate import validator

from pydantic import BaseModel, constr
from typing import Optional, List


class ResidenceAnimalsInput(BaseModel):
    animal: str
    quantidade: int


class ResidenceInput(BaseModel):
    cep: str
    municipio: str
    uf: constr(min_length=2, max_length=2)
    bairro: str
    tipo_logradouro: str
    nome_logradouro: str
    numero: str
    complemento: Optional[str] = None
    pto_referencia: Optional[str] = None
    microarea: str
    tipo_imovel: str
    telefone_residencia: Optional[str] = None
    telefone_contato: str
    situacao_moradia: str
    localizacao: str
    tipo_domicilio: str
    material_predominante: str
    condicao_posse_producao_rural: Optional[str] = None
    n_moradores: int
    n_comodos: int
    tipo_acesso: str
    energia_eletrica: bool
    abastecimento_agua: str
    escoamento_banheiro: str
    agua_consumo: str
    destino_lixo: str
    animais: Optional[List[ResidenceAnimalsInput]]

    def __init__(self, **data):
        super().__init__(**data)
        if self.uf:
            self.uf = self.uf.upper()


class ResidenceInputPatch(BaseModel):
    cep: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[constr(min_length=2, max_length=2)] = None
    bairro: Optional[str] = None
    tipo_logradouro: Optional[str] = None
    nome_logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    pto_referencia: Optional[str] = None
    microarea: Optional[str] = None
    tipo_imovel: Optional[str] = None
    telefone_residencia: Optional[str] = None
    telefone_contato: Optional[str] = None
    situacao_moradia: Optional[str] = None
    localizacao: Optional[str] = None
    tipo_domicilio: Optional[str] = None
    material_predominante: Optional[str] = None
    condicao_posse_producao_rural: Optional[str] = None
    n_moradores: Optional[int] = None
    n_comodos: Optional[int] = None
    tipo_acesso: Optional[str] = None
    energia_eletrica: Optional[bool] = None
    abastecimento_agua: Optional[str] = None
    escoamento_banheiro: Optional[str] = None
    agua_consumo: Optional[str] = None
    destino_lixo: Optional[str] = None
    animais: Optional[List[ResidenceAnimalsInput]] = None



STATES_MAP = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MS",
    "MT",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]
