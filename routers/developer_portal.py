from fastapi import APIRouter, Depends
from typing import List

from logic.public_api_logic import DeveloperPortalLogic
from persistency.schemas.public_api_schemas import (
    ApiKeyListItem,
    ApiKeyRevokeOutput,
    DeveloperLoginInput,
    DeveloperRegisterInput,
    DeveloperRegisterOutput,
    DeveloperSessionOutput,
)
from utils.helpers.validators.token_validator import validate_portal_session

developer_portal_router = APIRouter(prefix="/developer", tags=["developer-portal"])


@developer_portal_router.post(
    "/register",
    response_model=DeveloperRegisterOutput,
    status_code=201,
    description="Registra um novo desenvolvedor e gera sua primeira API key. A chave raw é retornada **uma única vez** — guarde-a.",
)
async def register_developer(body: DeveloperRegisterInput):
    return await DeveloperPortalLogic.register_developer_logic(
        name=body.name, email=body.email, password=body.password
    )


@developer_portal_router.post(
    "/auth/login",
    response_model=DeveloperSessionOutput,
    status_code=200,
    description="Autentica um desenvolvedor com e-mail e senha.",
)
async def login_developer(body: DeveloperLoginInput):
    return await DeveloperPortalLogic.login_developer_logic(
        email=body.email, password=body.password
    )


@developer_portal_router.get(
    "/keys",
    response_model=List[ApiKeyListItem],
    status_code=200,
    description="Lista as API keys do desenvolvedor autenticado.",
)
async def list_my_keys(developer_email: str = Depends(validate_portal_session)):
    return await DeveloperPortalLogic.list_developer_keys_logic(developer_email=developer_email)


@developer_portal_router.delete(
    "/keys/{key_id}",
    response_model=ApiKeyRevokeOutput,
    status_code=200,
    description="Revoga uma API key do desenvolvedor autenticado.",
)
async def revoke_my_key(
    key_id: int,
    developer_email: str = Depends(validate_portal_session),
):
    return await DeveloperPortalLogic.revoke_own_key_logic(
        key_id=key_id, developer_email=developer_email
    )
