from typing import List

from fastapi import APIRouter, Depends

from logic.public_api_logic import AdminApiKeyLogic
from persistency.schemas.public_api_schemas import (
    AdminApiKeyListItem,
    ApiKeyRevokeOutput,
    PaginatedLogs,
)
from utils.helpers.validators.token_validator import validate_session_admin

admin_api_keys_router = APIRouter(prefix="/admin/api-keys", tags=["admin"])


@admin_api_keys_router.get(
    "/",
    response_model=List[AdminApiKeyListItem],
    dependencies=[Depends(validate_session_admin)],
    description="Lista todas as API keys de desenvolvedores com contagem de uso.",
)
async def list_all_api_keys(page: int = 1, page_size: int = 20):
    return await AdminApiKeyLogic.list_all_keys_logic(page=page, page_size=page_size)


@admin_api_keys_router.patch(
    "/{key_id}/revoke",
    response_model=ApiKeyRevokeOutput,
    description="Revoga uma API key como administrador.",
)
async def admin_revoke_key(
    key_id: int,
    payload: dict = Depends(validate_session_admin),
):
    return await AdminApiKeyLogic.admin_revoke_key_logic(
        key_id=key_id, admin_email=payload["sub"]
    )


@admin_api_keys_router.get(
    "/{key_id}/logs",
    response_model=PaginatedLogs,
    dependencies=[Depends(validate_session_admin)],
    description="Logs de uso de uma API key específica.",
)
async def get_key_logs(key_id: int, page: int = 1, page_size: int = 50):
    return await AdminApiKeyLogic.get_key_logs_logic(
        key_id=key_id, page=page, page_size=page_size
    )
