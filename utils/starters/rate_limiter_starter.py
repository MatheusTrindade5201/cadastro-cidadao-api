from slowapi import Limiter
from slowapi.util import get_remote_address


def _get_api_key_or_ip(request):
    api_key = request.headers.get("X-API-Key")
    return api_key if api_key else get_remote_address(request)


limiter = Limiter(key_func=_get_api_key_or_ip)
