from starlette.requests import Request

from utils.exceptions.base import BaseInternalException, InternalServerError


async def internal_exception_handler(
    _: Request, exception: BaseInternalException
):
    return exception.generate_error_response()


async def server_error_handler(_: Request, exception: Exception):
    error_message = "Internal Server Error"
    return InternalServerError(
        name="Internal Server Error",
        description=exception.detail or error_message,
    ).generate_error_response()
