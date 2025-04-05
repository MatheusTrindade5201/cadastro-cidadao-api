from typing import List

from fastapi import APIRouter, FastAPI

from routers.home import home_router
from routers.login import login_router
from routers.users import user_router


class RouterDefiner:
    def __init__(self):
        self._routers: List[APIRouter] = [
            home_router,
            user_router,
            login_router
        ]

    def define_routers(self, app: FastAPI):
        for router in self._routers:
            app.include_router(router)
