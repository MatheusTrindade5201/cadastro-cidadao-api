from typing import List

from fastapi import APIRouter, FastAPI

from routers.admin_api_keys import admin_api_keys_router
from routers.developer_portal import developer_portal_router
from routers.home import home_router
from routers.individual import individual_router
from routers.login import login_router
from routers.public_api import public_router
from routers.residence import residence_router
from routers.users import user_router


class RouterDefiner:
    def __init__(self):
        self._routers: List[APIRouter] = [
            home_router,
            user_router,
            login_router,
            residence_router,
            individual_router,
            developer_portal_router,
            public_router,
            admin_api_keys_router,
        ]

    def define_routers(self, app: FastAPI):
        for router in self._routers:
            app.include_router(router)
