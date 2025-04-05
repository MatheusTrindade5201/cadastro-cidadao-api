from typing import Callable, List

from fastapi import FastAPI
from starlette.exceptions import HTTPException

from utils.exceptions.base import BaseInternalException
from utils.middlewares.exception_handler import (
    internal_exception_handler,
    server_error_handler,
)


class MiddlewareDefiner:
    def __init__(self):
        self._handlers: List[Callable] = [
            internal_exception_handler,
            server_error_handler,
        ]

    def define_handlers(self, app: FastAPI):
        for handler in self._handlers:
            if handler == internal_exception_handler:
                app.add_exception_handler(BaseInternalException, handler)
            else:
                app.add_exception_handler(HTTPException, handler)
