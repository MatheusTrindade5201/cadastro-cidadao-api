from fastapi import APIRouter

from logic.login_logic import LoginLogic
from persistency.schemas.login_schemas import (
    LoginInput,
    LoginOutput,

)

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.post(
    "/",
    description="Route to log into the system",
    status_code=200,
    response_model=LoginOutput,
)
async def login(login_data: LoginInput):
    return await LoginLogic.user_login_logic(login_data)


