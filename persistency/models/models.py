from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, ForeignKey, Boolean, Date
from sqlalchemy.dialects.mysql import DECIMAL

from persistency.connection import Base
from utils.helpers.time_helpers.utc_to_local import utc_to_local


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    created_at = Column(DateTime, default=lambda: utc_to_local(datetime.utcnow()))
    deleted_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=lambda: utc_to_local(datetime.utcnow()))
    role = Column(String)
    status = Column(SmallInteger, nullable=False, default=0)


class Domicilio(Base):
    __tablename__ = "domicilio"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    cep = Column(String(10), nullable=False)
    municipio = Column(String(60), nullable=False)
    uf = Column(String(2), nullable=False)
    bairro = Column(String(60), nullable=False)
    tipo_logradouro = Column(String(20), nullable=False)
    nome_logradouro = Column(String(60), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(20), nullable=True)
    pto_referencia = Column(String(60), nullable=True)
    microarea = Column(String(2), nullable=False)
    tipo_imovel = Column(String(2), nullable=False)
    telefone_residencia = Column(String(15), nullable=True)
    telefone_contato = Column(String(15), nullable=False)
    situacao_moradia = Column(String(20), nullable=False)
    localizacao = Column(String(60), nullable=False)
    tipo_domicilio = Column(String(60), nullable=False)
    material_predominante = Column(String(60), nullable=False)
    condicao_posse_producao_rural = Column(String(60), nullable=True)
    n_moradores = Column(Integer, nullable=False)
    n_comodos = Column(Integer, nullable=False)
    tipo_acesso = Column(String(60), nullable=False)
    energia_eletrica = Column(Boolean, nullable=False)
    abastecimento_agua = Column(String(60), nullable=False)
    escoamento_banheiro = Column(String(60), nullable=False)
    agua_consumo = Column(String(60), nullable=False)
    destino_lixo = Column(String(60), nullable=False)
    registered_by = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    last_updated_by = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    status = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: utc_to_local(datetime.utcnow()))
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, onupdate=lambda: utc_to_local(datetime.utcnow()), nullable=True)


class DomicilioAnimal(Base):
    __tablename__ = "domicilio_animal"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    domicilio_id = Column(Integer, ForeignKey("domicilio.id", ondelete="SET NULL"))
    animal = Column(String(60))
    quantidade = Column(Integer)


class Individuo(Base):
    __tablename__ = "individuo"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    cns = Column(String(60), nullable=False, unique=True)
    cpf = Column(String(60), nullable=False, unique=True)
    domicilio = Column(String(60), nullable=False)
    nome = Column(String(60), nullable=False)
    nome_social = Column(String(60), nullable=True)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String(1), nullable=False)
    raca_cor = Column(String(60), nullable=False)
    etnia = Column(String(60), nullable=False)
    nome_mae = Column(String(60), nullable=True)
    nome_pai = Column(String(60), nullable=True)
    nacionalidade = Column(String(60), nullable=False)
    pais = Column(String(60), nullable=False)
    data_naturalizacao = Column(Date, nullable=True)
    naturalizacao_portaria = Column(String(20), nullable=True)
    municipio_nascimento = Column(String(60), nullable=False)
    uf_nascimento = Column(String(2), nullable=False)
    entrada_brasil_data = Column(Date, nullable=True)
    celular = Column(String(15), nullable=False)
    email = Column(String(60), nullable=False)
    relacao_responsavel = Column(String(60), nullable=True)
    ocupacao = Column(String(60), nullable=True)
    frequenta_escola_creche = Column(Boolean, nullable=True)
    escolaridade = Column(String(60), nullable=True)
    situacao_mercado_trabalho = Column(String(60), nullable=True)
    frequenta_cuidador = Column(Boolean, nullable=True)
    participa_grupo_comunitario = Column(Boolean, nullable=True)
    plano_saude = Column(Boolean, nullable=True)
    membro_povo_comunidade_tradicional = Column(Boolean, nullable=True)
    orientacao_sexual = Column(String(60), nullable=True)
    identidade_genero = Column(String(60), nullable=True)
    motivo_saida = Column(String(60), nullable=True)
    data_saida = Column(Date, nullable=True)
    numero_declaracao_obito = Column(String(15), nullable=True)
    gestante = Column(Boolean, nullable=True)
    maternidade_referencia = Column(String(60), nullable=True)
    fumante = Column(Boolean, nullable=True)
    uso_alcool = Column(Boolean, nullable=True)
    uso_drogas = Column(Boolean, nullable=True)
    hipertensao = Column(Boolean, nullable=True)
    diabetes = Column(Boolean, nullable=True)
    avc_derrame = Column(Boolean, nullable=True)
    infarto = Column(Boolean, nullable=True)
    doenca_cardiaca = Column(Boolean, nullable=True)
    problemas_renais = Column(Boolean, nullable=True)
    hanseniase = Column(Boolean, nullable=True)
    doenca_respiratoria = Column(Boolean, nullable=True)
    tuberculose = Column(Boolean, nullable=True)
    cancer = Column(Boolean, nullable=True)
    internacao_recente = Column(Boolean, nullable=True)
    internacao_motivo = Column(String(60), nullable=True)
    diagnostico_problema_mental = Column(Boolean, nullable=True)
    acamado = Column(Boolean, nullable=True)
    domiciliado = Column(Boolean, nullable=True)
    praticas_ingestivas_complementares = Column(Boolean, nullable=True)
    registered_by = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    last_updated_by = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    status = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: utc_to_local(datetime.utcnow()), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, onupdate=lambda: utc_to_local(datetime.utcnow()), nullable=True)


class DomicilioIndividuo(Base):
    __tablename__ = "domicilio_individuo"
    domicilio_id = Column(Integer, ForeignKey("domicilio.id", ondelete="CASCADE"), primary_key=True)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"), primary_key=True)
    data_residencia = Column(Date)
    mudou = Column(Boolean)
    renda_familia_salario_minimos = Column(DECIMAL)
    n_membros_familia = Column(Integer)
    responsavel = Column(Boolean)


class CuidadorIndividuo(Base):
    __tablename__ = "cuidador_individuo"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"))
    cuidador = Column(String(60))


class IndividuoDeficiencia(Base):
    __tablename__ = "individuo_deficiencia"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"))
    deficiencia = Column(String(60))


class IndividuoCondicao(Base):
    __tablename__ = "individuo_condicao"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"))
    condicao = Column(String(60))


class IndividuoDoencaCardiaca(Base):
    __tablename__ = "individuo_doenca_cardiaca"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"))
    doenca = Column(String(60))


class IndividuoDoencaRespiratoria(Base):
    __tablename__ = "individuo_doenca_respiratoria"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"))
    doenca = Column(String(60))


class IndividuoDoencaRenal(Base):
    __tablename__ = "individuo_doenca_renal"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"))
    doenca = Column(String(60))


class IndividuoCondicaoRua(Base):
    __tablename__ = "individuo_condicao_rua"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    individuo_id = Column(Integer, ForeignKey("individuo.id", ondelete="CASCADE"))
    tempo = Column(String(60))
    recebe_beneficio = Column(Boolean)
    referencia_familiar = Column(Boolean)
    refeicoes_dia = Column(Integer)
    visita_familiar = Column(Boolean)
    graus_parentesco_familiar = Column(String(20))
    instituicao_apoio = Column(String(60))


class CondicaoRuaOrigemAlimentacao(Base):
    __tablename__ = "condicao_rua_origem_alimentacao"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    condicao_rua_id = Column(Integer, ForeignKey("individuo_condicao_rua.id", ondelete="CASCADE"))
    origem = Column(String(60))


class CondicaoRuaAcessoHigiene(Base):
    __tablename__ = "condicao_rua_acesso_higiene"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    condicao_rua_id = Column(Integer, ForeignKey("individuo_condicao_rua.id", ondelete="CASCADE"))
    acesso_higiene = Column(String(60))
