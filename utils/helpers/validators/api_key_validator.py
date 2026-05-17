from fastapi import Request, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from persistency.connection import get_db
from persistency.models.models import ApiKey
from service.public_api_service import ApiKeyService, ApiKeyUsageLogService
from utils.exceptions.exception import InvalidApiKey
from utils.providers.hash_provider import verify_hash

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def validate_api_key(
    request: Request,
    api_key_header: str = Security(API_KEY_HEADER),
) -> ApiKey:
    if not api_key_header:
        raise InvalidApiKey()

    parts = api_key_header.split("_")
    if len(parts) < 3:
        raise InvalidApiKey()
    prefix = parts[0] + "_" + parts[1]

    async with await get_db() as session:
        candidates = await ApiKeyService.find_key_by_prefix(prefix, session)
        matched_key: ApiKey = None
        for candidate in candidates:
            if verify_hash(api_key_header, candidate.key_hash):
                matched_key = candidate
                break

        if not matched_key:
            raise InvalidApiKey()

        await ApiKeyService.update_last_used(matched_key.id, session)
        await ApiKeyUsageLogService.log_request(
            api_key_id=matched_key.id,
            endpoint=str(request.url.path),
            method=request.method,
            status_code=200,
            ip_address=request.client.host if request.client else None,
            session=session,
        )
        await session.commit()

    return matched_key
