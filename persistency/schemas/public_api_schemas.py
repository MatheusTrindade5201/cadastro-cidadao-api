from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr


# ── Developer Portal ──────────────────────────────────────────────

class DeveloperRegisterInput(BaseModel):
    name: str
    email: EmailStr
    password: str


class DeveloperRegisterOutput(BaseModel):
    id: int
    name: str
    email: str
    api_key: str
    prefix: str
    created_at: datetime

    class Config:
        orm_mode = True


class DeveloperLoginInput(BaseModel):
    email: EmailStr
    password: str


class DeveloperSessionOutput(BaseModel):
    session_token: str
    developer_id: int
    email: str


class ApiKeyListItem(BaseModel):
    id: int
    prefix: str
    status: str
    last_used_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True


class ApiKeyRevokeOutput(BaseModel):
    id: int
    status: str
    revoked_at: Optional[datetime]

    class Config:
        orm_mode = True


# ── Admin ─────────────────────────────────────────────────────────

class AdminApiKeyListItem(BaseModel):
    id: int
    developer_id: int
    developer_email: str
    prefix: str
    status: str
    created_at: datetime
    last_used_at: Optional[datetime]
    usage_count: int


class AdminKeyLogItem(BaseModel):
    id: int
    endpoint: str
    method: str
    status_code: int
    requested_at: datetime
    ip_address: Optional[str]

    class Config:
        orm_mode = True


class PaginatedLogs(BaseModel):
    items: List[AdminKeyLogItem]
    total: int
    page: int
    page_size: int


# ── Public Stats ──────────────────────────────────────────────────

class PopulacaoStats(BaseModel):
    total: Optional[int]
    por_uf: Optional[Dict[str, Any]]
    por_municipio: Optional[Dict[str, Any]]
    por_sexo: Optional[Dict[str, Any]]
    por_raca_cor: Optional[Dict[str, Any]]


class FaixaEtariaStats(BaseModel):
    total: Optional[int]
    por_faixa: Optional[Dict[str, Any]]
    por_faixa_por_sexo: Optional[Dict[str, Any]]


class SaudeStats(BaseModel):
    total_individuos: Optional[int]
    fumante_pct: Optional[float]
    uso_alcool_pct: Optional[float]
    uso_drogas_pct: Optional[float]
    hipertensao_pct: Optional[float]
    diabetes_pct: Optional[float]
    avc_derrame_pct: Optional[float]
    infarto_pct: Optional[float]
    doenca_cardiaca_pct: Optional[float]
    problemas_renais_pct: Optional[float]
    hanseniase_pct: Optional[float]
    doenca_respiratoria_pct: Optional[float]
    tuberculose_pct: Optional[float]
    cancer_pct: Optional[float]
    internacao_recente_pct: Optional[float]
    diagnostico_problema_mental_pct: Optional[float]


class DoencasStats(BaseModel):
    total_individuos: Optional[int]
    doencas_cardiacas: Optional[Dict[str, Any]]
    doencas_respiratorias: Optional[Dict[str, Any]]
    doencas_renais: Optional[Dict[str, Any]]


class GestanteStats(BaseModel):
    total_gestantes: Optional[int]
    com_maternidade_referencia_pct: Optional[float]
    por_microarea: Optional[Dict[str, Any]]


class VulnerabilidadeStats(BaseModel):
    total_individuos: Optional[int]
    acamado_pct: Optional[float]
    domiciliado_pct: Optional[float]
    uso_alcool_pct: Optional[float]
    uso_drogas_pct: Optional[float]
    total_com_deficiencia: Optional[int]
    por_deficiencia: Optional[Dict[str, Any]]


class SocialStats(BaseModel):
    total_individuos: Optional[int]
    por_escolaridade: Optional[Dict[str, Any]]
    por_situacao_mercado_trabalho: Optional[Dict[str, Any]]
    frequenta_escola_creche_pct: Optional[float]
    participa_grupo_comunitario_pct: Optional[float]
    plano_saude_pct: Optional[float]
    membro_povo_tradicional_pct: Optional[float]


class ObitosStats(BaseModel):
    total: Optional[int]
    por_mes_ano: Optional[Dict[str, Any]]
    por_faixa_etaria: Optional[Dict[str, Any]]
    por_sexo: Optional[Dict[str, Any]]


class SituacaoRuaStats(BaseModel):
    total: Optional[int]
    por_tempo: Optional[Dict[str, Any]]
    recebe_beneficio_pct: Optional[float]
    sem_referencia_familiar_pct: Optional[float]
    por_origem_alimentacao: Optional[Dict[str, Any]]
    por_acesso_higiene: Optional[Dict[str, Any]]


class DomicilioStats(BaseModel):
    total_domicilios: Optional[int]
    por_tipo_domicilio: Optional[Dict[str, Any]]
    por_situacao_moradia: Optional[Dict[str, Any]]
    com_energia_eletrica_pct: Optional[float]
    por_abastecimento_agua: Optional[Dict[str, Any]]
    por_escoamento_banheiro: Optional[Dict[str, Any]]
    por_agua_consumo: Optional[Dict[str, Any]]
    por_destino_lixo: Optional[Dict[str, Any]]
    por_tipo_acesso: Optional[Dict[str, Any]]
    por_material_predominante: Optional[Dict[str, Any]]
    media_moradores: Optional[float]
    media_comodos: Optional[float]


class DomicilioRegionalStats(BaseModel):
    por_uf: Optional[Dict[str, Any]]
    por_municipio: Optional[Dict[str, Any]]
    por_microarea: Optional[Dict[str, Any]]
    media_moradores_por_municipio: Optional[Dict[str, Any]]
    densidade_por_municipio: Optional[Dict[str, Any]]


class AnimaisStats(BaseModel):
    total_domicilios_com_animais: Optional[int]
    por_tipo: Optional[Dict[str, Any]]
    total_por_tipo: Optional[Dict[str, Any]]


class MicroareaStats(BaseModel):
    por_microarea: Optional[Dict[str, Any]]
