#!/usr/bin/env python3
"""
Seed: ~500 registros para Guarulhos - SP
Uso: python seed.py
Requer DATABASE_URL no .env ou variável de ambiente.
"""
import asyncio
import os
import random
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal

from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from persistency.models.models import (
    CuidadorIndividuo,
    CondicaoRuaAcessoHigiene,
    CondicaoRuaOrigemAlimentacao,
    Domicilio,
    DomicilioAnimal,
    DomicilioIndividuo,
    Individuo,
    IndividuoCondicao,
    IndividuoCondicaoRua,
    IndividuoDeficiencia,
    IndividuoDoencaCardiaca,
    IndividuoDoencaRenal,
    IndividuoDoencaRespiratoria,
    User,
)

load_dotenv()
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:admin@localhost:5432/backend",
)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

random.seed(42)

# ─── Dados de Guarulhos ──────────────────────────────────────────────────────

BAIRROS = [
    ("Centro",                   "07010"),
    ("Vila Galvão",              "07040"),
    ("Gopouva",                  "07050"),
    ("Jardim São João",          "07060"),
    ("Vila Augusta",             "07070"),
    ("Macedo",                   "07080"),
    ("Ponte Grande",             "07090"),
    ("São João",                 "07100"),
    ("Vila das Palmeiras",       "07110"),
    ("Vila Rio de Janeiro",      "07120"),
    ("Jardim Fortaleza",         "07130"),
    ("Vila Endres",              "07140"),
    ("Paraventi",                "07150"),
    ("Bonsucesso",               "07160"),
    ("Itapegica",                "07170"),
    ("Cumbica",                  "07180"),
    ("Jardim Presidente Dutra",  "07190"),
    ("Jardim Bom Clima",         "07220"),
    ("Jardim Tranquilidade",     "07250"),
    ("Pimentas",                 "07240"),
]

LOGRADOUROS = [
    ("Rua", "das Flores"),          ("Rua", "dos Pinheiros"),
    ("Rua", "da Paz"),              ("Rua", "São José"),
    ("Rua", "das Acácias"),         ("Rua", "do Ipê"),
    ("Avenida", "Guarulhos"),       ("Avenida", "Salgado Filho"),
    ("Avenida", "Monteiro Lobato"), ("Avenida", "Tiradentes"),
    ("Rua", "Presidente Vargas"),   ("Rua", "Santos Dumont"),
    ("Travessa", "das Palmeiras"),  ("Rua", "Independência"),
    ("Rua", "Padre José"),          ("Avenida", "Brasil"),
    ("Rua", "Marechal Deodoro"),    ("Estrada", "Velha de Guarulhos"),
    ("Rua", "Conde Frontin"),       ("Alameda", "das Magnólias"),
    ("Rua", "XV de Novembro"),      ("Rua", "Sete de Setembro"),
    ("Avenida", "Coronel Ottoni"),  ("Rua", "Visconde de Taunaí"),
    ("Rua", "Barão do Rio Branco"),
]

NOMES_M = [
    "João", "José", "Antônio", "Carlos", "Francisco", "Paulo", "Pedro",
    "Lucas", "Luiz", "Marcos", "Gabriel", "Rafael", "Daniel", "Marcelo",
    "Eduardo", "Felipe", "Bruno", "Rodrigo", "Henrique", "Diego",
    "André", "Ricardo", "Alexandre", "Roberto", "Guilherme",
]
NOMES_F = [
    "Maria", "Ana", "Francisca", "Antônia", "Adriana", "Juliana", "Márcia",
    "Fernanda", "Patrícia", "Aline", "Sandra", "Camila", "Amanda", "Bruna",
    "Letícia", "Larissa", "Tatiane", "Luciana", "Michele", "Vanessa",
    "Cristiane", "Rosangela", "Eliane", "Sueli", "Claudia",
]
SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves",
    "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho",
    "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa",
    "Rocha", "Dias", "Nascimento", "Andrade", "Moreira",
    "Nunes", "Marques", "Machado", "Mendes", "Freitas",
]
OCUPACOES = [
    "Doméstico(a)", "Operário(a)", "Comerciante", "Motorista", "Pedreiro",
    "Professora", "Enfermeiro(a)", "Aposentado(a)", "Estudante", "Autônomo(a)",
    "Desempregado(a)", "Cozinheiro(a)", "Técnico(a)", "Vendedor(a)",
    "Segurança", "Faxineiro(a)", "Costureira", "Auxiliar administrativo",
]
ESCOLARIDADES = [
    "Sem escolaridade",
    "Ensino Fundamental Incompleto",
    "Ensino Fundamental Completo",
    "Ensino Médio Incompleto",
    "Ensino Médio Completo",
    "Ensino Superior Incompleto",
    "Ensino Superior Completo",
]
SITUACOES_MERCADO = [
    "Empregado com carteira", "Empregado sem carteira",
    "Autônomo", "Desempregado", "Aposentado/Pensionista", "Não se aplica",
]
MATERIAIS = [
    "Alvenaria/tijolo com revestimento",
    "Alvenaria/tijolo sem revestimento",
    "Adobe",
    "Madeira aparelhada",
    "Material aproveitado",
]
TIPOS_DOMICILIO = ["Casa", "Apartamento", "Cômodo/cortiço", "Improvisado"]
SITUACOES_MORADIA = ["Próprio", "Financiado", "Alugado", "Cedido", "Ocupação"]
ABASTECIMENTO = [
    "Rede encanada até o domicílio", "Poço ou nascente", "Cisternas", "Outros",
]
ESCOAMENTO = [
    "Rede coletora de esgoto ou pluvial", "Fossa séptica",
    "Fossa rudimentar", "Direto para vala/rio",
]
AGUA_CONSUMO = ["Filtrada", "Fervida", "Clorada", "Sem tratamento"]
DESTINO_LIXO = [
    "Coletado", "Queimado/enterrado no terreno",
    "Jogado em terreno baldio", "Outro destino",
]
LOCALIZACAO = ["Urbana", "Rural", "Periurbana"]
TIPOS_ACESSO = ["Pavimento", "Chão batido", "Outro"]
MICROAREAS = ["MA1", "MA2", "MA3", "MA4", "MA5", "MA6"]
ANIMAIS = ["Cão", "Gato", "Galinha", "Porco", "Pássaro", "Coelho"]
DEFICIENCIAS = [
    "Visual", "Auditiva", "Intelectual/cognitiva", "Física", "Psicossocial",
]
CONDICOES = [
    "Acúmulo de lixo", "Criança com baixo peso",
    "Criança com excesso de peso", "Adulto com obesidade",
    "Idoso com demência", "Uso de tabaco",
]
DOENCAS_CARDIACAS = [
    "Insuficiência cardíaca", "Coronariopatia", "Valvulopatia", "Arritmia",
]
DOENCAS_RESP = ["Asma", "DPOC", "Bronquite", "Rinite alérgica"]
DOENCAS_RENAIS = [
    "Insuficiência renal crônica", "Cálculo renal", "Nefrite",
]
CUIDADORES = [
    "Cônjuge", "Filho(a)", "Pai/Mãe", "Irmão/Irmã",
    "Outro familiar", "Cuidador profissional",
]
ORIGENS_ALIM = [
    "Restaurante popular", "Cozinha comunitária", "Doação",
    "Obtida em restaurantes", "Obtida em supermercado", "Outros",
]
ACESSOS_HIGIENE = [
    "Banheiro público", "Albergue", "Posto de saúde",
    "Igreja/entidade religiosa", "Não tem acesso",
]
RELACOES_RESPONSAVEL = [
    "Cônjuge", "Filho(a)", "Irmão/Irmã", "Pai/Mãe",
    "Avô/Avó", "Outro parente", "Não parente",
]
MOTIVOS_SAIDA = [
    "Mudança de território", "Óbito",
    "Institucionalização", "Mudança de município",
]
RACAS = ["Branca", "Preta", "Parda", "Amarela", "Indígena"]
ETNIAS = ["Não informada", "Indígena", "Quilombola", "Não se aplica"]
MUNICIPIOS_NASCIMENTO = [
    "Guarulhos", "São Paulo", "Mogi das Cruzes", "Suzano",
    "Arujá", "Santa Isabel", "Mairiporã", "Cajamar",
    "Francisco Morato", "Franco da Rocha",
]
ORIENTACOES = ["Heterossexual", "Homossexual", "Bissexual", "Não informado"]
IDENTIDADES = [
    "Travesti", "Transexual homem", "Transexual mulher", "Não informado",
]
TEMPOS_RUA = [
    "Menos de 6 meses", "6 a 12 meses",
    "1 a 2 anos", "2 a 5 anos", "Mais de 5 anos",
]

# ─── Helpers ─────────────────────────────────────────────────────────────────

_cpfs_used: set = set()
_cns_used: set = set()


def rnd_cpf() -> str:
    while True:
        v = "".join(str(random.randint(0, 9)) for _ in range(11))
        if v not in _cpfs_used:
            _cpfs_used.add(v)
            return v


def rnd_cns() -> str:
    while True:
        v = "".join(str(random.randint(0, 9)) for _ in range(15))
        if v not in _cns_used:
            _cns_used.add(v)
            return v


def rnd_date(start: int = 1940, end: int = 2008) -> date:
    s = date(start, 1, 1)
    e = date(end, 12, 31)
    return s + timedelta(days=random.randint(0, (e - s).days))


def rnd_phone() -> str:
    return f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"


def rnd_cep(prefix: str) -> str:
    return f"{prefix}{random.randint(0, 9):01d}-{random.randint(0, 999):03d}"


def rnd_nome(sexo: str) -> str:
    first = random.choice(NOMES_M if sexo == "M" else NOMES_F)
    return f"{first} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"


def w(prob: float = 0.3) -> bool:
    return random.random() < prob


def maybe(value, prob: float = 0.4):
    return value if random.random() < prob else None


NOW = datetime(2026, 4, 25, 8, 0, 0)

# ─── Builders ────────────────────────────────────────────────────────────────

def build_users() -> list[User]:
    agentes = [
        ("Ana Paula Ferreira",    "ana.paula@ubs-guarulhos.sp.gov.br"),
        ("Carlos Eduardo Lima",   "carlos.lima@ubs-guarulhos.sp.gov.br"),
        ("Márcia Souza",          "marcia.souza@ubs-guarulhos.sp.gov.br"),
        ("Roberto Alves",         "roberto.alves@ubs-guarulhos.sp.gov.br"),
        ("Juliana Costa",         "juliana.costa@ubs-guarulhos.sp.gov.br"),
        ("Diego Martins",         "diego.martins@ubs-guarulhos.sp.gov.br"),
        ("Fernanda Ribeiro",      "fernanda.ribeiro@ubs-guarulhos.sp.gov.br"),
        ("Paulo Nascimento",      "paulo.nascimento@ubs-guarulhos.sp.gov.br"),
        ("Sandra Oliveira",       "sandra.oliveira@ubs-guarulhos.sp.gov.br"),
        ("Rodrigo Gomes",         "rodrigo.gomes@ubs-guarulhos.sp.gov.br"),
    ]
    users = []
    hashed = pwd_context.hash("Guarulhos@2026")
    for name, email in agentes:
        users.append(User(
            name=name,
            email=email,
            password=hashed,
            role="ACS",
            status=1,
            created_at=NOW,
        ))
    admin = User(
        name="Administrador UBS",
        email="admin@ubs-guarulhos.sp.gov.br",
        password=pwd_context.hash("Admin@2026!"),
        role="ADMIN",
        status=1,
        created_at=NOW,
    )
    users.append(admin)
    return users


def build_domicilios(user_ids: list[int], n: int = 160) -> list[Domicilio]:
    domicilios = []
    for _ in range(n):
        bairro, cep_prefix = random.choice(BAIRROS)
        tipo_log, nome_log = random.choice(LOGRADOUROS)
        has_animals = w(0.25)
        domicilios.append(Domicilio(
            cep=rnd_cep(cep_prefix),
            municipio="Guarulhos",
            uf="SP",
            bairro=bairro,
            tipo_logradouro=tipo_log,
            nome_logradouro=nome_log,
            numero=str(random.randint(1, 999)),
            complemento=maybe(random.choice(["Apto 12", "Casa B", "Fundos", "Bloco A"]), 0.25),
            pto_referencia=maybe(random.choice([
                "Próximo ao mercado", "Em frente à escola",
                "Perto da UBS", "Ao lado da praça",
            ]), 0.3),
            microarea=random.choice(MICROAREAS),
            tipo_imovel=random.choice(["01", "02", "03"]),
            telefone_residencia=maybe(rnd_phone(), 0.4),
            telefone_contato=rnd_phone(),
            situacao_moradia=random.choices(
                SITUACOES_MORADIA, weights=[30, 15, 40, 10, 5], k=1
            )[0],
            localizacao=random.choices(
                LOCALIZACAO, weights=[80, 5, 15], k=1
            )[0],
            tipo_domicilio=random.choices(
                TIPOS_DOMICILIO, weights=[65, 20, 10, 5], k=1
            )[0],
            material_predominante=random.choices(
                MATERIAIS, weights=[55, 25, 5, 10, 5], k=1
            )[0],
            condicao_posse_producao_rural=maybe("Assentado", 0.05),
            n_moradores=random.choices(
                [1, 2, 3, 4, 5, 6, 7], weights=[8, 18, 25, 25, 14, 7, 3], k=1
            )[0],
            n_comodos=random.randint(2, 8),
            tipo_acesso=random.choices(
                TIPOS_ACESSO, weights=[70, 20, 10], k=1
            )[0],
            energia_eletrica=w(0.92),
            abastecimento_agua=random.choices(
                ABASTECIMENTO, weights=[80, 8, 7, 5], k=1
            )[0],
            escoamento_banheiro=random.choices(
                ESCOAMENTO, weights=[65, 20, 10, 5], k=1
            )[0],
            agua_consumo=random.choices(
                AGUA_CONSUMO, weights=[40, 15, 30, 15], k=1
            )[0],
            destino_lixo=random.choices(
                DESTINO_LIXO, weights=[80, 8, 7, 5], k=1
            )[0],
            registered_by=random.choice(user_ids),
            last_updated_by=random.choice(user_ids),
            status=1,
            created_at=NOW - timedelta(days=random.randint(0, 365)),
        ))
    return domicilios


def build_animais(domicilio_ids: list[int]) -> list[DomicilioAnimal]:
    animais = []
    for d_id in domicilio_ids:
        if w(0.28):
            n = random.randint(1, 2)
            escolhidos = random.sample(ANIMAIS, min(n, len(ANIMAIS)))
            for animal in escolhidos:
                animais.append(DomicilioAnimal(
                    domicilio_id=d_id,
                    animal=animal,
                    quantidade=random.randint(1, 4),
                ))
    return animais


def build_individuo(user_ids: list[int], domicilio_ref: str) -> Individuo:
    sexo = random.choice(["M", "F"])
    nome = rnd_nome(sexo)
    nascimento = rnd_date(1930, 2020)

    is_rua = w(0.04)
    saiu = w(0.05)
    tem_saude_mental = w(0.08)
    tem_hipertensao = w(0.22)
    tem_diabetes = w(0.12)
    tem_doenca_cardiaca = w(0.10)
    tem_doenca_resp = w(0.10)
    tem_problemas_renais = w(0.07)

    return Individuo(
        cns=rnd_cns(),
        cpf=rnd_cpf(),
        domicilio=domicilio_ref,
        nome=nome,
        nome_social=maybe(rnd_nome(sexo), 0.03),
        data_nascimento=nascimento,
        sexo=sexo,
        raca_cor=random.choices(RACAS, weights=[42, 10, 43, 2, 3], k=1)[0],
        etnia=random.choices(ETNIAS, weights=[75, 5, 5, 15], k=1)[0],
        nome_mae=maybe(rnd_nome("F"), 0.85),
        nome_pai=maybe(rnd_nome("M"), 0.55),
        nacionalidade=random.choices(
            ["Brasileiro", "Estrangeiro"], weights=[90, 10], k=1
        )[0],
        pais="Brasil",
        data_naturalizacao=None,
        naturalizacao_portaria=None,
        municipio_nascimento=random.choices(
            MUNICIPIOS_NASCIMENTO,
            weights=[40, 30, 5, 5, 3, 3, 3, 3, 4, 4],
            k=1,
        )[0],
        uf_nascimento="SP",
        entrada_brasil_data=None,
        celular=rnd_phone(),
        email=f"{nome.split()[0].lower()}.{random.randint(10,999)}@email.com",
        relacao_responsavel=maybe(random.choice(RELACOES_RESPONSAVEL), 0.5),
        ocupacao=maybe(random.choice(OCUPACOES), 0.75),
        frequenta_escola_creche=maybe(w(0.35), 0.6),
        escolaridade=maybe(random.choice(ESCOLARIDADES), 0.8),
        situacao_mercado_trabalho=maybe(random.choice(SITUACOES_MERCADO), 0.75),
        frequenta_cuidador=maybe(w(0.15), 0.5),
        participa_grupo_comunitario=maybe(w(0.20), 0.5),
        plano_saude=maybe(w(0.20), 0.6),
        membro_povo_comunidade_tradicional=maybe(w(0.03), 0.4),
        orientacao_sexual=maybe(random.choice(ORIENTACOES), 0.3),
        identidade_genero=maybe(random.choice(IDENTIDADES), 0.3),
        motivo_saida=random.choice(MOTIVOS_SAIDA) if saiu else None,
        data_saida=(NOW.date() - timedelta(days=random.randint(30, 300))) if saiu else None,
        numero_declaracao_obito=maybe(
            f"DO{random.randint(100000,999999)}", 0.02
        ),
        gestante=(w(0.08) if sexo == "F" else None),
        maternidade_referencia=maybe("UBS Jardim São João", 0.1),
        fumante=maybe(w(0.18), 0.7),
        uso_alcool=maybe(w(0.15), 0.7),
        uso_drogas=maybe(w(0.06), 0.6),
        hipertensao=tem_hipertensao if w(0.8) else None,
        diabetes=tem_diabetes if w(0.8) else None,
        avc_derrame=maybe(w(0.05), 0.6),
        infarto=maybe(w(0.05), 0.6),
        doenca_cardiaca=tem_doenca_cardiaca if w(0.8) else None,
        problemas_renais=tem_problemas_renais if w(0.8) else None,
        hanseniase=maybe(w(0.02), 0.5),
        doenca_respiratoria=tem_doenca_resp if w(0.8) else None,
        tuberculose=maybe(w(0.02), 0.5),
        cancer=maybe(w(0.04), 0.5),
        internacao_recente=maybe(w(0.10), 0.6),
        internacao_motivo=maybe(random.choice([
            "Cirurgia", "Infecção", "Acidente", "Parto", "Crise hipertensiva",
        ]), 0.3),
        diagnostico_problema_mental=tem_saude_mental if w(0.8) else None,
        acamado=maybe(w(0.05), 0.5),
        domiciliado=maybe(w(0.08), 0.5),
        praticas_ingestivas_complementares=maybe(w(0.07), 0.4),
        registered_by=random.choice(user_ids),
        last_updated_by=random.choice(user_ids),
        status=0 if saiu else 1,
        created_at=NOW - timedelta(days=random.randint(0, 365)),
    )


def build_domicilio_individuo(
    domicilio_id: int, individuo_id: int, responsavel: bool
) -> DomicilioIndividuo:
    return DomicilioIndividuo(
        domicilio_id=domicilio_id,
        individuo_id=individuo_id,
        data_residencia=rnd_date(2010, 2025),
        mudou=w(0.10),
        renda_familia_salario_minimos=Decimal(
            str(round(random.choices(
                [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0],
                weights=[10, 35, 25, 15, 8, 5, 2],
                k=1,
            )[0], 1))
        ),
        n_membros_familia=random.randint(1, 7),
        responsavel=responsavel,
    )


def build_deficiencias(individuo_id: int) -> list[IndividuoDeficiencia]:
    if not w(0.12):
        return []
    n = random.choices([1, 2], weights=[80, 20], k=1)[0]
    return [
        IndividuoDeficiencia(individuo_id=individuo_id, deficiencia=d)
        for d in random.sample(DEFICIENCIAS, n)
    ]


def build_condicoes(individuo_id: int) -> list[IndividuoCondicao]:
    if not w(0.15):
        return []
    return [
        IndividuoCondicao(individuo_id=individuo_id, condicao=random.choice(CONDICOES))
    ]


def build_doenca_cardiaca(individuo_id: int, has: bool) -> list[IndividuoDoencaCardiaca]:
    if not has:
        return []
    return [
        IndividuoDoencaCardiaca(
            individuo_id=individuo_id, doenca=random.choice(DOENCAS_CARDIACAS)
        )
    ]


def build_doenca_resp(individuo_id: int, has: bool) -> list[IndividuoDoencaRespiratoria]:
    if not has:
        return []
    return [
        IndividuoDoencaRespiratoria(
            individuo_id=individuo_id, doenca=random.choice(DOENCAS_RESP)
        )
    ]


def build_doenca_renal(individuo_id: int, has: bool) -> list[IndividuoDoencaRenal]:
    if not has:
        return []
    return [
        IndividuoDoencaRenal(
            individuo_id=individuo_id, doenca=random.choice(DOENCAS_RENAIS)
        )
    ]


def build_cuidador(individuo_id: int, is_acamado: bool) -> list[CuidadorIndividuo]:
    if not (is_acamado and w(0.7)):
        return []
    return [
        CuidadorIndividuo(
            individuo_id=individuo_id, cuidador=random.choice(CUIDADORES)
        )
    ]


def build_condicao_rua(
    individuo_id: int
) -> tuple[IndividuoCondicaoRua | None, list, list]:
    rua = IndividuoCondicaoRua(
        individuo_id=individuo_id,
        tempo=random.choice(TEMPOS_RUA),
        recebe_beneficio=w(0.35),
        referencia_familiar=w(0.45),
        refeicoes_dia=random.randint(1, 3),
        visita_familiar=w(0.30),
        graus_parentesco_familiar=maybe(random.choice([
            "Filho(a)", "Cônjuge", "Irmão/Irmã", "Pai/Mãe",
        ]), 0.5),
        instituicao_apoio=maybe(random.choice([
            "CRAS Guarulhos", "Albergue Municipal", "Igreja São Paulo",
            "SAMU", "Pastoral da Rua",
        ]), 0.6),
    )
    return rua


# ─── Main ────────────────────────────────────────────────────────────────────

async def seed():
    engine = create_async_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        print("→ Criando usuários (agentes ACS)...")
        users = build_users()
        session.add_all(users)
        await session.flush()
        user_ids = [u.id for u in users]
        print(f"  {len(users)} usuários inseridos.")

        print("→ Criando domicílios...")
        domicilios = build_domicilios(user_ids, n=160)
        session.add_all(domicilios)
        await session.flush()
        domicilio_ids = [d.id for d in domicilios]
        print(f"  {len(domicilios)} domicílios inseridos.")

        print("→ Criando animais por domicílio...")
        animais = build_animais(domicilio_ids)
        session.add_all(animais)
        print(f"  {len(animais)} registros de animais inseridos.")

        print("→ Criando indivíduos e vínculos...")
        individuos_total = 0
        vinculos_total = 0
        sub_total = {
            "deficiencias": 0, "condicoes": 0,
            "cardiacas": 0, "resp": 0, "renais": 0,
            "cuidadores": 0, "condicao_rua": 0,
        }

        for domicilio in domicilios:
            n_moradores = domicilio.n_moradores
            n_individuos = min(n_moradores, random.randint(1, min(n_moradores, 5)))

            endereco_ref = (
                f"{domicilio.tipo_logradouro} {domicilio.nome_logradouro}, "
                f"{domicilio.numero} - {domicilio.bairro}, Guarulhos/SP"
            )

            for i in range(n_individuos):
                ind = build_individuo(user_ids, endereco_ref)
                session.add(ind)
                await session.flush()
                individuos_total += 1

                vinculo = build_domicilio_individuo(
                    domicilio.id, ind.id, responsavel=(i == 0)
                )
                session.add(vinculo)
                vinculos_total += 1

                for obj in build_deficiencias(ind.id):
                    session.add(obj)
                    sub_total["deficiencias"] += 1

                for obj in build_condicoes(ind.id):
                    session.add(obj)
                    sub_total["condicoes"] += 1

                for obj in build_doenca_cardiaca(ind.id, bool(ind.doenca_cardiaca)):
                    session.add(obj)
                    sub_total["cardiacas"] += 1

                for obj in build_doenca_resp(ind.id, bool(ind.doenca_respiratoria)):
                    session.add(obj)
                    sub_total["resp"] += 1

                for obj in build_doenca_renal(ind.id, bool(ind.problemas_renais)):
                    session.add(obj)
                    sub_total["renais"] += 1

                for obj in build_cuidador(ind.id, bool(ind.acamado)):
                    session.add(obj)
                    sub_total["cuidadores"] += 1

                if w(0.04):
                    rua = build_condicao_rua(ind.id)
                    session.add(rua)
                    await session.flush()
                    sub_total["condicao_rua"] += 1

                    n_orig = random.randint(1, 3)
                    for orig in random.sample(ORIGENS_ALIM, n_orig):
                        session.add(CondicaoRuaOrigemAlimentacao(
                            condicao_rua_id=rua.id, origem=orig
                        ))

                    n_hig = random.randint(1, 2)
                    for hig in random.sample(ACESSOS_HIGIENE, n_hig):
                        session.add(CondicaoRuaAcessoHigiene(
                            condicao_rua_id=rua.id, acesso_higiene=hig
                        ))

        await session.commit()

        print(f"  {individuos_total} indivíduos inseridos.")
        print(f"  {vinculos_total} vínculos domicílio-indivíduo inseridos.")
        print()
        print("─── Subtabelas ─────────────────────────────────")
        print(f"  Deficiências:        {sub_total['deficiencias']}")
        print(f"  Condições:           {sub_total['condicoes']}")
        print(f"  Doenças cardíacas:   {sub_total['cardiacas']}")
        print(f"  Doenças resp.:       {sub_total['resp']}")
        print(f"  Doenças renais:      {sub_total['renais']}")
        print(f"  Cuidadores:          {sub_total['cuidadores']}")
        print(f"  Condição de rua:     {sub_total['condicao_rua']}")
        print("─────────────────────────────────────────────────")
        print()
        print("Seed concluído com sucesso!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
