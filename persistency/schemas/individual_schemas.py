from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, List
from datetime import date

class CondicaoRuaInput(BaseModel):
    tempo: Optional[str]
    recebe_beneficio: Optional[bool]
    referencia_familiar: Optional[bool]
    refeicoes_dia: Optional[int]
    visita_familiar: Optional[bool]
    graus_parentesco_familiar: Optional[str]
    instituicao_apoio: Optional[str]
    origem_alimentacao: Optional[List[str]]
    acesso_higiene: Optional[List[str]]


class IndividualInput(BaseModel):
    cns: constr(max_length=60)
    cpf: constr(max_length=60)
    domicilio: constr(max_length=60)
    nome: constr(max_length=60)
    nome_social: Optional[constr(max_length=60)] = None
    data_nascimento: date
    sexo: constr(max_length=1)
    raca_cor: constr(max_length=60)
    etnia: constr(max_length=60)
    nome_mae: Optional[constr(max_length=60)] = None
    nome_pai: Optional[constr(max_length=60)] = None
    nacionalidade: constr(max_length=60)
    pais: constr(max_length=60)
    data_naturalizacao: Optional[date] = None
    naturalizacao_portaria: Optional[constr(max_length=20)] = None
    municipio_nascimento: constr(max_length=60)
    uf_nascimento: constr(max_length=2)
    entrada_brasil_data: Optional[date] = None
    celular: constr(max_length=15)
    email: EmailStr
    relacao_responsavel: Optional[constr(max_length=60)] = None
    ocupacao: Optional[constr(max_length=60)] = None
    frequenta_escola_creche: Optional[bool] = None
    escolaridade: Optional[constr(max_length=60)] = None
    situacao_mercado_trabalho: Optional[constr(max_length=60)] = None
    frequenta_cuidador: Optional[bool] = None
    participa_grupo_comunitario: Optional[bool] = None
    plano_saude: Optional[bool] = None
    membro_povo_comunidade_tradicional: Optional[bool] = None
    orientacao_sexual: Optional[constr(max_length=60)] = None
    identidade_genero: Optional[constr(max_length=60)] = None
    motivo_saida: Optional[constr(max_length=60)] = None
    data_saida: Optional[date] = None
    numero_declaracao_obito: Optional[constr(max_length=15)] = None
    gestante: Optional[bool] = None
    maternidade_referencia: Optional[constr(max_length=60)] = None
    fumante: Optional[bool] = None
    uso_alcool: Optional[bool] = None
    uso_drogas: Optional[bool] = None
    hipertensao: Optional[bool] = None
    diabetes: Optional[bool] = None
    avc_derrame: Optional[bool] = None
    infarto: Optional[bool] = None
    doenca_cardiaca: Optional[bool] = None
    problemas_renais: Optional[bool] = None
    hanseniase: Optional[bool] = None
    doenca_respiratoria: Optional[bool] = None
    tuberculose: Optional[bool] = None
    cancer: Optional[bool] = None
    internacao_recente: Optional[bool] = None
    internacao_motivo: Optional[constr(max_length=60)] = None
    diagnostico_problema_mental: Optional[bool] = None
    acamado: Optional[bool] = None
    domiciliado: Optional[bool] = None
    praticas_ingestivas_complementares: Optional[bool] = None

    cuidadores: Optional[List[str]]
    condicoes: Optional[List[str]]
    deficiencias: Optional[List[str]]
    doencas_cardiacas: Optional[List[str]]
    doencas_respiratorias: Optional[List[str]]
    doencas_renais: Optional[List[str]]
    condicao_rua: Optional[CondicaoRuaInput]
