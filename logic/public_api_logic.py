import secrets
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from persistency.schemas.public_api_schemas import (
    AdminApiKeyListItem,
    ApiKeyListItem,
    ApiKeyRevokeOutput,
    AnimaisStats,
    DeveloperRegisterOutput,
    DeveloperSessionOutput,
    DomicilioRegionalStats,
    DomicilioStats,
    DoencasStats,
    FaixaEtariaStats,
    GestanteStats,
    MicroareaStats,
    ObitosStats,
    PaginatedLogs,
    PopulacaoStats,
    SaudeStats,
    SituacaoRuaStats,
    SocialStats,
    VulnerabilidadeStats,
)

from service.public_api_service import (
    ApiKeyService,
    ApiKeyUsageLogService,
    DeveloperService,
    PublicStatsService,
)
from service.user_services import UserService
from utils.exceptions.exception import (
    ApiKeyAlreadyRevoked,
    DeveloperAlreadyExists,
    EntityNotExists,
    ForbiddenToken,
    UnauthorizedLogin,
)
from utils.middlewares.session_controller import TransactionSession
from utils.providers.hash_provider import generate_hash, verify_hash
from utils.providers.token_provider import jwt_encoder


class DeveloperPortalLogic:

    @staticmethod
    @TransactionSession()
    async def register_developer_logic(
        name: str, email: str, password: str, session: AsyncSession
    ) -> DeveloperRegisterOutput:
        existing = await DeveloperService.get_developer_by_email(email, session)
        if existing:
            raise DeveloperAlreadyExists()

        password_hash = generate_hash(password)
        developer = await DeveloperService.create_developer(name, email, password_hash, session)

        random_part = secrets.token_urlsafe(32)
        prefix = "cc_" + random_part[:8]
        raw_key = prefix + "_" + random_part[8:]
        key_hash = generate_hash(raw_key)

        await ApiKeyService.create_api_key(developer.id, prefix, key_hash, session)

        return DeveloperRegisterOutput(
            id=developer.id,
            name=developer.name,
            email=developer.email,
            api_key=raw_key,
            prefix=prefix,
            created_at=developer.created_at,
        )

    @staticmethod
    @TransactionSession()
    async def login_developer_logic(
        email: str, password: str, session: AsyncSession
    ) -> DeveloperSessionOutput:
        developer = await DeveloperService.get_developer_by_email(email, session)
        if not developer or not developer.password_hash:
            raise UnauthorizedLogin("invalid credentials")

        if not verify_hash(password, developer.password_hash):
            raise UnauthorizedLogin("invalid credentials")

        session_token = jwt_encoder({"sub": developer.email, "type": "portal_session"}, exp=1440)

        return DeveloperSessionOutput(
            session_token=session_token,
            developer_id=developer.id,
            email=developer.email,
        )

    @staticmethod
    @TransactionSession()
    async def list_developer_keys_logic(
        developer_email: str, session: AsyncSession
    ) -> List[ApiKeyListItem]:
        developer = await DeveloperService.get_developer_by_email(developer_email, session)
        if not developer:
            raise EntityNotExists("Developer not found")

        keys = await ApiKeyService.get_keys_by_developer(developer.id, session)
        return [
            ApiKeyListItem(
                id=k.id,
                prefix=k.prefix,
                status=k.status,
                last_used_at=k.last_used_at,
                created_at=k.created_at,
            )
            for k in keys
        ]

    @staticmethod
    @TransactionSession()
    async def revoke_own_key_logic(
        key_id: int, developer_email: str, session: AsyncSession
    ) -> ApiKeyRevokeOutput:
        developer = await DeveloperService.get_developer_by_email(developer_email, session)
        if not developer:
            raise EntityNotExists("Developer not found")

        key = await ApiKeyService.get_key_by_id(key_id, session)
        if not key:
            raise EntityNotExists("API key not found")

        if key.developer_id != developer.id:
            raise ForbiddenToken("Key does not belong to this developer")

        if key.status == "revoked":
            raise ApiKeyAlreadyRevoked()

        updated_key = await ApiKeyService.revoke_key(key_id, revoked_by=None, session=session)
        return ApiKeyRevokeOutput(
            id=updated_key.id,
            status=updated_key.status,
            revoked_at=updated_key.revoked_at,
        )


class AdminApiKeyLogic:

    @staticmethod
    @TransactionSession()
    async def list_all_keys_logic(
        page: int, page_size: int, session: AsyncSession
    ) -> List[AdminApiKeyListItem]:
        rows = await ApiKeyService.get_all_keys_with_usage(page, page_size, session)
        return [
            AdminApiKeyListItem(
                id=r["id"],
                developer_id=r["developer_id"],
                developer_email=r["developer_email"],
                prefix=r["prefix"],
                status=r["status"],
                created_at=r["created_at"],
                last_used_at=r["last_used_at"],
                usage_count=r["usage_count"],
            )
            for r in rows
        ]

    @staticmethod
    @TransactionSession()
    async def admin_revoke_key_logic(
        key_id: int, admin_email: str, session: AsyncSession
    ) -> ApiKeyRevokeOutput:
        admin = await UserService.get_user(admin_email)
        key = await ApiKeyService.get_key_by_id(key_id, session)
        if not key:
            raise EntityNotExists("API key not found")

        if key.status == "revoked":
            raise ApiKeyAlreadyRevoked()

        updated_key = await ApiKeyService.revoke_key(
            key_id, revoked_by=admin.id if admin else None, session=session
        )
        return ApiKeyRevokeOutput(
            id=updated_key.id,
            status=updated_key.status,
            revoked_at=updated_key.revoked_at,
        )

    @staticmethod
    @TransactionSession()
    async def get_key_logs_logic(
        key_id: int, page: int, page_size: int, session: AsyncSession
    ) -> PaginatedLogs:
        key = await ApiKeyService.get_key_by_id(key_id, session)
        if not key:
            raise EntityNotExists("API key not found")

        items, total = await ApiKeyUsageLogService.get_logs_by_key(key_id, page, page_size, session)
        return PaginatedLogs(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )


class PublicStatsLogic:

    @staticmethod
    @TransactionSession()
    async def get_populacao_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> PopulacaoStats:
        data = await PublicStatsService.get_populacao_stats(uf, municipio, session)
        return PopulacaoStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_faixas_etarias_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> FaixaEtariaStats:
        data = await PublicStatsService.get_faixas_etarias_stats(uf, municipio, session)
        return FaixaEtariaStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_saude_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> SaudeStats:
        data = await PublicStatsService.get_saude_stats(uf, municipio, session)
        return SaudeStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_doencas_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> DoencasStats:
        data = await PublicStatsService.get_doencas_stats(uf, municipio, session)
        return DoencasStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_gestante_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> GestanteStats:
        data = await PublicStatsService.get_gestante_stats(uf, municipio, session)
        return GestanteStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_vulnerabilidade_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> VulnerabilidadeStats:
        data = await PublicStatsService.get_vulnerabilidade_stats(uf, municipio, session)
        return VulnerabilidadeStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_social_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> SocialStats:
        data = await PublicStatsService.get_social_stats(uf, municipio, session)
        return SocialStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_obitos_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> ObitosStats:
        data = await PublicStatsService.get_obitos_stats(uf, municipio, session)
        return ObitosStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_situacao_rua_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> SituacaoRuaStats:
        data = await PublicStatsService.get_situacao_rua_stats(uf, municipio, session)
        return SituacaoRuaStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_domicilio_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> DomicilioStats:
        data = await PublicStatsService.get_domicilio_stats(uf, municipio, session)
        return DomicilioStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_domicilio_regional_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> DomicilioRegionalStats:
        data = await PublicStatsService.get_domicilio_regional_stats(uf, municipio, session)
        return DomicilioRegionalStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_animais_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> AnimaisStats:
        data = await PublicStatsService.get_animais_stats(uf, municipio, session)
        return AnimaisStats(**data)

    @staticmethod
    @TransactionSession()
    async def get_microarea_logic(
        uf: Optional[str], municipio: Optional[str], session: AsyncSession
    ) -> MicroareaStats:
        data = await PublicStatsService.get_microarea_stats(uf, municipio, session)
        return MicroareaStats(**data)
