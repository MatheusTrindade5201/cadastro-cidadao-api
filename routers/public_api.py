from typing import Optional

from fastapi import APIRouter, Depends, Request

from logic.public_api_logic import PublicStatsLogic
from persistency.models.models import ApiKey
from persistency.schemas.public_api_schemas import (
    AnimaisStats,
    DomicilioRegionalStats,
    DomicilioStats,
    DoencasStats,
    FaixaEtariaStats,
    GestanteStats,
    MicroareaStats,
    ObitosStats,
    PopulacaoStats,
    SaudeStats,
    SituacaoRuaStats,
    SocialStats,
    VulnerabilidadeStats,
)
from utils.helpers.validators.api_key_validator import validate_api_key
from utils.starters.rate_limiter_starter import limiter

public_router = APIRouter(prefix="/public/v1", tags=["public-api"])

_RATE = "100/hour"
_AUTH = [Depends(validate_api_key)]


@public_router.get(
    "/stats/populacao",
    response_model=PopulacaoStats,
    dependencies=_AUTH,
    description="Estatísticas populacionais agregadas. Valores com menos de 5 registros retornam null (regra de anonimidade).",
)
@limiter.limit(_RATE)
async def get_populacao(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_populacao_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/populacao/faixas-etarias",
    response_model=FaixaEtariaStats,
    dependencies=_AUTH,
    description="Distribuição por faixa etária (0-4, 5-9, ..., 80+).",
)
@limiter.limit(_RATE)
async def get_faixas_etarias(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_faixas_etarias_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/saude",
    response_model=SaudeStats,
    dependencies=_AUTH,
    description="Prevalência percentual de condições crônicas de saúde.",
)
@limiter.limit(_RATE)
async def get_saude(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_saude_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/saude/doencas",
    response_model=DoencasStats,
    dependencies=_AUTH,
    description="Breakdown detalhado de doenças cardíacas, respiratórias e renais.",
)
@limiter.limit(_RATE)
async def get_doencas(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_doencas_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/saude/gestantes",
    response_model=GestanteStats,
    dependencies=_AUTH,
    description="Estatísticas de gestantes por microárea e referência de maternidade.",
)
@limiter.limit(_RATE)
async def get_gestantes(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_gestante_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/saude/vulnerabilidade",
    response_model=VulnerabilidadeStats,
    dependencies=_AUTH,
    description="Indicadores de vulnerabilidade: acamados, domiciliados, deficiências.",
)
@limiter.limit(_RATE)
async def get_vulnerabilidade(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_vulnerabilidade_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/social",
    response_model=SocialStats,
    dependencies=_AUTH,
    description="Indicadores sociais: escolaridade, mercado de trabalho, participação comunitária.",
)
@limiter.limit(_RATE)
async def get_social(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_social_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/social/obitos",
    response_model=ObitosStats,
    dependencies=_AUTH,
    description="Óbitos registrados por período, faixa etária e sexo.",
)
@limiter.limit(_RATE)
async def get_obitos(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_obitos_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/social/situacao-rua",
    response_model=SituacaoRuaStats,
    dependencies=_AUTH,
    description="Estatísticas de pessoas em situação de rua: tempo, benefícios, alimentação e higiene.",
)
@limiter.limit(_RATE)
async def get_situacao_rua(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_situacao_rua_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/domicilios",
    response_model=DomicilioStats,
    dependencies=_AUTH,
    description="Infraestrutura habitacional: tipo de domicílio, saneamento, energia e médias.",
)
@limiter.limit(_RATE)
async def get_domicilios(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_domicilio_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/domicilios/por-regiao",
    response_model=DomicilioRegionalStats,
    dependencies=_AUTH,
    description="Distribuição regional de domicílios: por UF, município e microárea, com densidade.",
)
@limiter.limit(_RATE)
async def get_domicilios_por_regiao(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_domicilio_regional_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/animais",
    response_model=AnimaisStats,
    dependencies=_AUTH,
    description="Animais por domicílio: total de domicílios com animais, por tipo e quantidade.",
)
@limiter.limit(_RATE)
async def get_animais(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_animais_logic(uf=uf, municipio=municipio)


@public_router.get(
    "/stats/microareas",
    response_model=MicroareaStats,
    dependencies=_AUTH,
    description="Contagem de domicílios e indivíduos por microárea.",
)
@limiter.limit(_RATE)
async def get_microareas(
    request: Request,
    uf: Optional[str] = None,
    municipio: Optional[str] = None,
):
    return await PublicStatsLogic.get_microarea_logic(uf=uf, municipio=municipio)
