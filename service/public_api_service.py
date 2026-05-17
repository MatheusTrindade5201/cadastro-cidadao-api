from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import case, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from persistency.models.models import (
    ApiKey,
    ApiKeyDeveloper,
    ApiKeyUsageLog,
    CondicaoRuaAcessoHigiene,
    CondicaoRuaOrigemAlimentacao,
    DeveloperSession,
    Domicilio,
    DomicilioAnimal,
    DomicilioIndividuo,
    Individuo,
    IndividuoCondicaoRua,
    IndividuoDeficiencia,
    IndividuoDoencaCardiaca,
    IndividuoDoencaRenal,
    IndividuoDoencaRespiratoria,
)
from utils.helpers.time_helpers.utc_to_local import utc_to_local


ANONYMITY_THRESHOLD = 5


def _null_if_below(count: Optional[int]) -> Optional[int]:
    if count is None:
        return None
    return count if count >= ANONYMITY_THRESHOLD else None


def _filter_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    return {k: (_null_if_below(v) if isinstance(v, int) else v) for k, v in d.items()}


def _pct(positive: int, total: int) -> Optional[float]:
    if total < ANONYMITY_THRESHOLD:
        return None
    return round(positive / total * 100, 2) if total > 0 else 0.0


class DeveloperService:
    @staticmethod
    async def get_developer_by_email(email: str, session: AsyncSession) -> Optional[ApiKeyDeveloper]:
        result = await session.execute(
            select(ApiKeyDeveloper).where(ApiKeyDeveloper.email == email)
        )
        return result.scalars().first()

    @staticmethod
    async def create_developer(name: str, email: str, password_hash: str, session: AsyncSession) -> ApiKeyDeveloper:
        developer = ApiKeyDeveloper(name=name, email=email, password_hash=password_hash)
        session.add(developer)
        await session.flush()
        return developer

    @staticmethod
    async def get_developer_by_id(developer_id: int, session: AsyncSession) -> Optional[ApiKeyDeveloper]:
        result = await session.execute(
            select(ApiKeyDeveloper).where(ApiKeyDeveloper.id == developer_id)
        )
        return result.scalars().first()


class ApiKeyService:
    @staticmethod
    async def create_api_key(
        developer_id: int, prefix: str, key_hash: str, session: AsyncSession
    ) -> ApiKey:
        api_key = ApiKey(developer_id=developer_id, prefix=prefix, key_hash=key_hash)
        session.add(api_key)
        await session.flush()
        return api_key

    @staticmethod
    async def get_keys_by_developer(developer_id: int, session: AsyncSession) -> List[ApiKey]:
        result = await session.execute(
            select(ApiKey)
            .where(ApiKey.developer_id == developer_id)
            .order_by(ApiKey.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_key_by_id(key_id: int, session: AsyncSession) -> Optional[ApiKey]:
        result = await session.execute(
            select(ApiKey).where(ApiKey.id == key_id)
        )
        return result.scalars().first()

    @staticmethod
    async def revoke_key(key_id: int, revoked_by: Optional[int], session: AsyncSession) -> ApiKey:
        now = utc_to_local(datetime.utcnow())
        await session.execute(
            update(ApiKey)
            .where(ApiKey.id == key_id)
            .values(status="revoked", revoked_at=now, revoked_by=revoked_by)
        )
        await session.flush()
        result = await session.execute(select(ApiKey).where(ApiKey.id == key_id))
        return result.scalars().first()

    @staticmethod
    async def find_key_by_prefix(prefix: str, session: AsyncSession) -> List[ApiKey]:
        result = await session.execute(
            select(ApiKey).where(ApiKey.prefix == prefix, ApiKey.status == "active")
        )
        return result.scalars().all()

    @staticmethod
    async def update_last_used(key_id: int, session: AsyncSession) -> None:
        now = utc_to_local(datetime.utcnow())
        await session.execute(
            update(ApiKey).where(ApiKey.id == key_id).values(last_used_at=now)
        )

    @staticmethod
    async def get_all_keys_with_usage(
        page: int, page_size: int, session: AsyncSession
    ) -> List[Dict[str, Any]]:
        offset = (page - 1) * page_size
        usage_subq = (
            select(ApiKeyUsageLog.api_key_id, func.count(ApiKeyUsageLog.id).label("usage_count"))
            .group_by(ApiKeyUsageLog.api_key_id)
            .subquery()
        )
        result = await session.execute(
            select(
                ApiKey.id,
                ApiKey.developer_id,
                ApiKeyDeveloper.email.label("developer_email"),
                ApiKey.prefix,
                ApiKey.status,
                ApiKey.created_at,
                ApiKey.last_used_at,
                func.coalesce(usage_subq.c.usage_count, 0).label("usage_count"),
            )
            .join(ApiKeyDeveloper, ApiKey.developer_id == ApiKeyDeveloper.id)
            .outerjoin(usage_subq, ApiKey.id == usage_subq.c.api_key_id)
            .order_by(ApiKey.created_at.desc())
            .limit(page_size)
            .offset(offset)
        )
        rows = result.fetchall()
        return [row._mapping for row in rows]


class ApiKeyUsageLogService:
    @staticmethod
    async def log_request(
        api_key_id: int,
        endpoint: str,
        method: str,
        status_code: int,
        ip_address: Optional[str],
        session: AsyncSession,
    ) -> None:
        log = ApiKeyUsageLog(
            api_key_id=api_key_id,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            ip_address=ip_address,
        )
        session.add(log)

    @staticmethod
    async def get_logs_by_key(
        key_id: int, page: int, page_size: int, session: AsyncSession
    ) -> Tuple[List[ApiKeyUsageLog], int]:
        offset = (page - 1) * page_size
        count_result = await session.execute(
            select(func.count(ApiKeyUsageLog.id)).where(ApiKeyUsageLog.api_key_id == key_id)
        )
        total = count_result.scalar()

        result = await session.execute(
            select(ApiKeyUsageLog)
            .where(ApiKeyUsageLog.api_key_id == key_id)
            .order_by(ApiKeyUsageLog.requested_at.desc())
            .limit(page_size)
            .offset(offset)
        )
        items = result.scalars().all()
        return items, total


class DeveloperSessionService:
    @staticmethod
    async def create_session(
        developer_id: int, token_hash: str, expires_at: datetime, session: AsyncSession
    ) -> DeveloperSession:
        dev_session = DeveloperSession(
            developer_id=developer_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        session.add(dev_session)
        await session.flush()
        return dev_session

    @staticmethod
    async def get_valid_session_by_token_hash(
        token_hash: str, session: AsyncSession
    ) -> Optional[DeveloperSession]:
        now = utc_to_local(datetime.utcnow())
        result = await session.execute(
            select(DeveloperSession).where(
                DeveloperSession.token_hash == token_hash,
                DeveloperSession.used_at.is_(None),
                DeveloperSession.expires_at > now,
            )
        )
        return result.scalars().first()

    @staticmethod
    async def mark_session_used(session_id: int, db_session: AsyncSession) -> None:
        now = utc_to_local(datetime.utcnow())
        await db_session.execute(
            update(DeveloperSession)
            .where(DeveloperSession.id == session_id)
            .values(used_at=now)
        )


# ── Stats ─────────────────────────────────────────────────────────

def _apply_filters(query, uf: Optional[str], municipio: Optional[str], model=Individuo):
    if uf:
        if model == Individuo:
            query = query.where(Individuo.uf_nascimento == uf)
        elif model == Domicilio:
            query = query.where(Domicilio.uf == uf)
    if municipio:
        if model == Individuo:
            query = query.where(Individuo.municipio_nascimento == municipio)
        elif model == Domicilio:
            query = query.where(Domicilio.municipio == municipio)
    return query


class PublicStatsService:

    @staticmethod
    async def get_populacao_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        base = select(func.count(Individuo.id)).where(Individuo.status == 0)
        base = _apply_filters(base, uf, municipio)
        total = (await session.execute(base)).scalar() or 0

        async def group_by_col(col):
            q = _apply_filters(
                select(col, func.count(Individuo.id)).where(Individuo.status == 0).group_by(col),
                uf, municipio,
            )
            rows = (await session.execute(q)).fetchall()
            return _filter_dict({str(r[0]): r[1] for r in rows if r[0]})

        return {
            "total": _null_if_below(total),
            "por_uf": await group_by_col(Individuo.uf_nascimento),
            "por_municipio": await group_by_col(Individuo.municipio_nascimento),
            "por_sexo": await group_by_col(Individuo.sexo),
            "por_raca_cor": await group_by_col(Individuo.raca_cor),
        }

    @staticmethod
    async def get_faixas_etarias_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        faixas = [
            ("0-4", 0, 4), ("5-9", 5, 9), ("10-14", 10, 14), ("15-19", 15, 19),
            ("20-29", 20, 29), ("30-39", 30, 39), ("40-49", 40, 49),
            ("50-59", 50, 59), ("60-69", 60, 69), ("70-79", 70, 79), ("80+", 80, 200),
        ]
        hoje = datetime.utcnow().date()

        por_faixa = {}
        for label, low, high in faixas:
            q = select(func.count(Individuo.id)).where(
                Individuo.status == 0,
                func.date_part("year", func.age(hoje, Individuo.data_nascimento)) >= low,
                func.date_part("year", func.age(hoje, Individuo.data_nascimento)) <= high,
            )
            q = _apply_filters(q, uf, municipio)
            cnt = (await session.execute(q)).scalar() or 0
            por_faixa[label] = _null_if_below(cnt)

        total_q = _apply_filters(
            select(func.count(Individuo.id)).where(Individuo.status == 0), uf, municipio
        )
        total = (await session.execute(total_q)).scalar() or 0

        return {"total": _null_if_below(total), "por_faixa": por_faixa, "por_faixa_por_sexo": None}

    @staticmethod
    async def get_saude_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        total_q = _apply_filters(
            select(func.count(Individuo.id)).where(Individuo.status == 0), uf, municipio
        )
        total = (await session.execute(total_q)).scalar() or 0

        bool_fields = [
            "fumante", "uso_alcool", "uso_drogas", "hipertensao", "diabetes",
            "avc_derrame", "infarto", "doenca_cardiaca", "problemas_renais",
            "hanseniase", "doenca_respiratoria", "tuberculose", "cancer",
            "internacao_recente", "diagnostico_problema_mental",
        ]

        result: Dict[str, Any] = {"total_individuos": _null_if_below(total)}
        for field in bool_fields:
            col = getattr(Individuo, field)
            q = _apply_filters(
                select(func.count(Individuo.id)).where(Individuo.status == 0, col == True),
                uf, municipio,
            )
            positive = (await session.execute(q)).scalar() or 0
            result[f"{field}_pct"] = _pct(positive, total)

        return result

    @staticmethod
    async def get_doencas_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        total_q = _apply_filters(
            select(func.count(Individuo.id)).where(Individuo.status == 0), uf, municipio
        )
        total = (await session.execute(total_q)).scalar() or 0

        async def doenca_group(model, join_col):
            subq = select(Individuo.id)
            if uf or municipio:
                subq = _apply_filters(subq.where(Individuo.status == 0), uf, municipio)
            q = (
                select(model.doenca, func.count(model.id))
                .where(model.individuo_id.in_(subq))
                .group_by(model.doenca)
            )
            rows = (await session.execute(q)).fetchall()
            return _filter_dict({str(r[0]): r[1] for r in rows if r[0]})

        return {
            "total_individuos": _null_if_below(total),
            "doencas_cardiacas": await doenca_group(IndividuoDoencaCardiaca, IndividuoDoencaCardiaca.individuo_id),
            "doencas_respiratorias": await doenca_group(IndividuoDoencaRespiratoria, IndividuoDoencaRespiratoria.individuo_id),
            "doencas_renais": await doenca_group(IndividuoDoencaRenal, IndividuoDoencaRenal.individuo_id),
        }

    @staticmethod
    async def get_gestante_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        base = _apply_filters(
            select(func.count(Individuo.id)).where(Individuo.status == 0, Individuo.gestante == True),
            uf, municipio,
        )
        total_gestantes = (await session.execute(base)).scalar() or 0

        com_ref_q = _apply_filters(
            select(func.count(Individuo.id)).where(
                Individuo.status == 0,
                Individuo.gestante == True,
                Individuo.maternidade_referencia.isnot(None),
            ),
            uf, municipio,
        )
        com_ref = (await session.execute(com_ref_q)).scalar() or 0

        microarea_q = (
            select(Domicilio.microarea, func.count(Individuo.id))
            .join(DomicilioIndividuo, DomicilioIndividuo.individuo_id == Individuo.id)
            .join(Domicilio, Domicilio.id == DomicilioIndividuo.domicilio_id)
            .where(Individuo.status == 0, Individuo.gestante == True)
            .group_by(Domicilio.microarea)
        )
        if uf:
            microarea_q = microarea_q.where(Domicilio.uf == uf)
        if municipio:
            microarea_q = microarea_q.where(Domicilio.municipio == municipio)
        microarea_rows = (await session.execute(microarea_q)).fetchall()
        por_microarea = _filter_dict({str(r[0]): r[1] for r in microarea_rows if r[0]})

        return {
            "total_gestantes": _null_if_below(total_gestantes),
            "com_maternidade_referencia_pct": _pct(com_ref, total_gestantes),
            "por_microarea": por_microarea,
        }

    @staticmethod
    async def get_vulnerabilidade_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        total_q = _apply_filters(
            select(func.count(Individuo.id)).where(Individuo.status == 0), uf, municipio
        )
        total = (await session.execute(total_q)).scalar() or 0

        result: Dict[str, Any] = {"total_individuos": _null_if_below(total)}
        for field in ["acamado", "domiciliado", "uso_alcool", "uso_drogas"]:
            col = getattr(Individuo, field)
            q = _apply_filters(
                select(func.count(Individuo.id)).where(Individuo.status == 0, col == True),
                uf, municipio,
            )
            positive = (await session.execute(q)).scalar() or 0
            result[f"{field}_pct"] = _pct(positive, total)

        # Deficiências
        subq = select(Individuo.id)
        if uf or municipio:
            subq = _apply_filters(subq.where(Individuo.status == 0), uf, municipio)
        else:
            subq = subq.where(Individuo.status == 0)

        total_def_q = select(func.count(IndividuoDeficiencia.id)).where(
            IndividuoDeficiencia.individuo_id.in_(subq)
        )
        total_def = (await session.execute(total_def_q)).scalar() or 0

        def_group_q = (
            select(IndividuoDeficiencia.deficiencia, func.count(IndividuoDeficiencia.id))
            .where(IndividuoDeficiencia.individuo_id.in_(subq))
            .group_by(IndividuoDeficiencia.deficiencia)
        )
        def_rows = (await session.execute(def_group_q)).fetchall()
        por_deficiencia = _filter_dict({str(r[0]): r[1] for r in def_rows if r[0]})

        result["total_com_deficiencia"] = _null_if_below(total_def)
        result["por_deficiencia"] = por_deficiencia
        return result

    @staticmethod
    async def get_social_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        total_q = _apply_filters(
            select(func.count(Individuo.id)).where(Individuo.status == 0), uf, municipio
        )
        total = (await session.execute(total_q)).scalar() or 0

        async def group_col(col):
            q = _apply_filters(
                select(col, func.count(Individuo.id)).where(Individuo.status == 0).group_by(col),
                uf, municipio,
            )
            rows = (await session.execute(q)).fetchall()
            return _filter_dict({str(r[0]): r[1] for r in rows if r[0]})

        result: Dict[str, Any] = {"total_individuos": _null_if_below(total)}
        result["por_escolaridade"] = await group_col(Individuo.escolaridade)
        result["por_situacao_mercado_trabalho"] = await group_col(Individuo.situacao_mercado_trabalho)

        for field in ["frequenta_escola_creche", "participa_grupo_comunitario", "plano_saude", "membro_povo_comunidade_tradicional"]:
            col = getattr(Individuo, field)
            q = _apply_filters(
                select(func.count(Individuo.id)).where(Individuo.status == 0, col == True),
                uf, municipio,
            )
            positive = (await session.execute(q)).scalar() or 0
            result[f"{field}_pct"] = _pct(positive, total)

        return result

    @staticmethod
    async def get_obitos_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        base_where = [
            Individuo.status == 0,
            Individuo.numero_declaracao_obito.isnot(None),
        ]
        total_q = _apply_filters(
            select(func.count(Individuo.id)).where(*base_where), uf, municipio
        )
        total = (await session.execute(total_q)).scalar() or 0

        # Por mês/ano de saída
        mes_ano_q = _apply_filters(
            select(
                func.to_char(Individuo.data_saida, "YYYY-MM").label("mes_ano"),
                func.count(Individuo.id),
            )
            .where(*base_where, Individuo.data_saida.isnot(None))
            .group_by("mes_ano"),
            uf, municipio,
        )
        mes_rows = (await session.execute(mes_ano_q)).fetchall()
        por_mes_ano = _filter_dict({str(r[0]): r[1] for r in mes_rows if r[0]})

        # Por sexo
        sexo_q = _apply_filters(
            select(Individuo.sexo, func.count(Individuo.id))
            .where(*base_where)
            .group_by(Individuo.sexo),
            uf, municipio,
        )
        sexo_rows = (await session.execute(sexo_q)).fetchall()
        por_sexo = _filter_dict({str(r[0]): r[1] for r in sexo_rows if r[0]})

        hoje = datetime.utcnow().date()
        faixas = [
            ("0-17", 0, 17), ("18-39", 18, 39), ("40-59", 40, 59), ("60-79", 60, 79), ("80+", 80, 200),
        ]
        por_faixa: Dict[str, Any] = {}
        for label, low, high in faixas:
            q = _apply_filters(
                select(func.count(Individuo.id)).where(
                    *base_where,
                    func.date_part("year", func.age(hoje, Individuo.data_nascimento)) >= low,
                    func.date_part("year", func.age(hoje, Individuo.data_nascimento)) <= high,
                ),
                uf, municipio,
            )
            cnt = (await session.execute(q)).scalar() or 0
            por_faixa[label] = _null_if_below(cnt)

        return {
            "total": _null_if_below(total),
            "por_mes_ano": por_mes_ano,
            "por_faixa_etaria": por_faixa,
            "por_sexo": por_sexo,
        }

    @staticmethod
    async def get_situacao_rua_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        # Subquery para ids dos indivíduos filtrados
        ind_subq = select(Individuo.id).where(Individuo.status == 0)
        if uf:
            ind_subq = ind_subq.where(Individuo.uf_nascimento == uf)
        if municipio:
            ind_subq = ind_subq.where(Individuo.municipio_nascimento == municipio)

        total_q = select(func.count(IndividuoCondicaoRua.id)).where(
            IndividuoCondicaoRua.individuo_id.in_(ind_subq)
        )
        total = (await session.execute(total_q)).scalar() or 0

        tempo_q = (
            select(IndividuoCondicaoRua.tempo, func.count(IndividuoCondicaoRua.id))
            .where(IndividuoCondicaoRua.individuo_id.in_(ind_subq))
            .group_by(IndividuoCondicaoRua.tempo)
        )
        tempo_rows = (await session.execute(tempo_q)).fetchall()
        por_tempo = _filter_dict({str(r[0]): r[1] for r in tempo_rows if r[0]})

        benef_q = select(func.count(IndividuoCondicaoRua.id)).where(
            IndividuoCondicaoRua.individuo_id.in_(ind_subq),
            IndividuoCondicaoRua.recebe_beneficio == True,
        )
        benef = (await session.execute(benef_q)).scalar() or 0

        sem_ref_q = select(func.count(IndividuoCondicaoRua.id)).where(
            IndividuoCondicaoRua.individuo_id.in_(ind_subq),
            IndividuoCondicaoRua.referencia_familiar == False,
        )
        sem_ref = (await session.execute(sem_ref_q)).scalar() or 0

        # Origem alimentação
        rua_ids_q = select(IndividuoCondicaoRua.id).where(
            IndividuoCondicaoRua.individuo_id.in_(ind_subq)
        )
        orig_q = (
            select(CondicaoRuaOrigemAlimentacao.origem, func.count(CondicaoRuaOrigemAlimentacao.id))
            .where(CondicaoRuaOrigemAlimentacao.condicao_rua_id.in_(rua_ids_q))
            .group_by(CondicaoRuaOrigemAlimentacao.origem)
        )
        orig_rows = (await session.execute(orig_q)).fetchall()
        por_orig = _filter_dict({str(r[0]): r[1] for r in orig_rows if r[0]})

        # Acesso higiene
        hig_q = (
            select(CondicaoRuaAcessoHigiene.acesso_higiene, func.count(CondicaoRuaAcessoHigiene.id))
            .where(CondicaoRuaAcessoHigiene.condicao_rua_id.in_(rua_ids_q))
            .group_by(CondicaoRuaAcessoHigiene.acesso_higiene)
        )
        hig_rows = (await session.execute(hig_q)).fetchall()
        por_hig = _filter_dict({str(r[0]): r[1] for r in hig_rows if r[0]})

        return {
            "total": _null_if_below(total),
            "por_tempo": por_tempo,
            "recebe_beneficio_pct": _pct(benef, total),
            "sem_referencia_familiar_pct": _pct(sem_ref, total),
            "por_origem_alimentacao": por_orig,
            "por_acesso_higiene": por_hig,
        }

    @staticmethod
    async def get_domicilio_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        base_where = [Domicilio.status == 0, Domicilio.deleted_at.is_(None)]

        def apply_dom_filters(q):
            if uf:
                q = q.where(Domicilio.uf == uf)
            if municipio:
                q = q.where(Domicilio.municipio == municipio)
            return q

        total_q = apply_dom_filters(select(func.count(Domicilio.id)).where(*base_where))
        total = (await session.execute(total_q)).scalar() or 0

        avg_q = apply_dom_filters(
            select(func.avg(Domicilio.n_moradores), func.avg(Domicilio.n_comodos)).where(*base_where)
        )
        avg_row = (await session.execute(avg_q)).fetchone()
        media_moradores = round(float(avg_row[0]), 2) if avg_row and avg_row[0] else None
        media_comodos = round(float(avg_row[1]), 2) if avg_row and avg_row[1] else None

        energia_q = apply_dom_filters(
            select(func.count(Domicilio.id)).where(*base_where, Domicilio.energia_eletrica == True)
        )
        com_energia = (await session.execute(energia_q)).scalar() or 0

        async def dom_group(col):
            q = apply_dom_filters(
                select(col, func.count(Domicilio.id)).where(*base_where).group_by(col)
            )
            rows = (await session.execute(q)).fetchall()
            return _filter_dict({str(r[0]): r[1] for r in rows if r[0]})

        return {
            "total_domicilios": _null_if_below(total),
            "por_tipo_domicilio": await dom_group(Domicilio.tipo_domicilio),
            "por_situacao_moradia": await dom_group(Domicilio.situacao_moradia),
            "com_energia_eletrica_pct": _pct(com_energia, total),
            "por_abastecimento_agua": await dom_group(Domicilio.abastecimento_agua),
            "por_escoamento_banheiro": await dom_group(Domicilio.escoamento_banheiro),
            "por_agua_consumo": await dom_group(Domicilio.agua_consumo),
            "por_destino_lixo": await dom_group(Domicilio.destino_lixo),
            "por_tipo_acesso": await dom_group(Domicilio.tipo_acesso),
            "por_material_predominante": await dom_group(Domicilio.material_predominante),
            "media_moradores": media_moradores if (total or 0) >= ANONYMITY_THRESHOLD else None,
            "media_comodos": media_comodos if (total or 0) >= ANONYMITY_THRESHOLD else None,
        }

    @staticmethod
    async def get_domicilio_regional_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        base_where = [Domicilio.status == 0, Domicilio.deleted_at.is_(None)]

        def apply_dom_filters(q):
            if uf:
                q = q.where(Domicilio.uf == uf)
            if municipio:
                q = q.where(Domicilio.municipio == municipio)
            return q

        async def group_dom(col):
            q = apply_dom_filters(
                select(col, func.count(Domicilio.id)).where(*base_where).group_by(col)
            )
            rows = (await session.execute(q)).fetchall()
            return _filter_dict({str(r[0]): r[1] for r in rows if r[0]})

        async def avg_by(col):
            q = apply_dom_filters(
                select(col, func.avg(Domicilio.n_moradores)).where(*base_where).group_by(col)
            )
            rows = (await session.execute(q)).fetchall()
            return {str(r[0]): round(float(r[1]), 2) if r[1] else None for r in rows if r[0]}

        async def densidade_by(col):
            q = apply_dom_filters(
                select(
                    col,
                    (func.avg(Domicilio.n_moradores) / func.nullif(func.avg(Domicilio.n_comodos), 0)).label("dens"),
                )
                .where(*base_where)
                .group_by(col)
            )
            rows = (await session.execute(q)).fetchall()
            return {str(r[0]): round(float(r[1]), 2) if r[1] else None for r in rows if r[0]}

        return {
            "por_uf": await group_dom(Domicilio.uf),
            "por_municipio": await group_dom(Domicilio.municipio),
            "por_microarea": await group_dom(Domicilio.microarea),
            "media_moradores_por_municipio": await avg_by(Domicilio.municipio),
            "densidade_por_municipio": await densidade_by(Domicilio.municipio),
        }

    @staticmethod
    async def get_animais_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        dom_ids_q = select(Domicilio.id).where(
            Domicilio.status == 0, Domicilio.deleted_at.is_(None)
        )
        if uf:
            dom_ids_q = dom_ids_q.where(Domicilio.uf == uf)
        if municipio:
            dom_ids_q = dom_ids_q.where(Domicilio.municipio == municipio)

        total_dom_q = select(func.count(func.distinct(DomicilioAnimal.domicilio_id))).where(
            DomicilioAnimal.domicilio_id.in_(dom_ids_q)
        )
        total_dom = (await session.execute(total_dom_q)).scalar() or 0

        tipo_count_q = (
            select(DomicilioAnimal.animal, func.count(DomicilioAnimal.id))
            .where(DomicilioAnimal.domicilio_id.in_(dom_ids_q))
            .group_by(DomicilioAnimal.animal)
        )
        tipo_rows = (await session.execute(tipo_count_q)).fetchall()
        por_tipo = _filter_dict({str(r[0]): r[1] for r in tipo_rows if r[0]})

        total_por_tipo_q = (
            select(DomicilioAnimal.animal, func.sum(DomicilioAnimal.quantidade))
            .where(DomicilioAnimal.domicilio_id.in_(dom_ids_q))
            .group_by(DomicilioAnimal.animal)
        )
        tot_rows = (await session.execute(total_por_tipo_q)).fetchall()
        total_por_tipo = {str(r[0]): int(r[1]) if r[1] else 0 for r in tot_rows if r[0]}

        return {
            "total_domicilios_com_animais": _null_if_below(total_dom),
            "por_tipo": por_tipo,
            "total_por_tipo": total_por_tipo,
        }

    @staticmethod
    async def get_microarea_stats(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> Dict[str, Any]:
        q = (
            select(
                Domicilio.microarea,
                func.count(func.distinct(Domicilio.id)).label("total_domicilios"),
                func.count(func.distinct(DomicilioIndividuo.individuo_id)).label("total_individuos"),
            )
            .outerjoin(DomicilioIndividuo, DomicilioIndividuo.domicilio_id == Domicilio.id)
            .where(Domicilio.status == 0, Domicilio.deleted_at.is_(None))
            .group_by(Domicilio.microarea)
        )
        if uf:
            q = q.where(Domicilio.uf == uf)
        if municipio:
            q = q.where(Domicilio.municipio == municipio)

        rows = (await session.execute(q)).fetchall()
        por_microarea: Dict[str, Any] = {}
        for r in rows:
            microarea = str(r[0]) if r[0] else "?"
            doms = _null_if_below(r[1])
            inds = _null_if_below(r[2])
            por_microarea[microarea] = {"domicilios": doms, "individuos": inds}

        return {"por_microarea": por_microarea}
